import os
import re
import sys
import subprocess
import json
from env import *


def query_metadata(src_file):
    """
    metadata of the selected item.
    :param str src_file: source file.
    :return: src_file's metadata.
    """
    cmds = [
        "{}/ffprobe".format(config['ffmpeg']),
        "-loglevel",
        "0",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        src_file,
        "-hide_banner"
    ]

    process = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    meta_dict = json.loads(process.communicate()[0])
    meta_dict_new = {}
    meta_dict_new['first'] = 1
    if meta_dict['streams'][0]['avg_frame_rate'] == '0/0':
        meta_dict_new['last'] = meta_dict['streams'][1]['nb_frames']
        meta_dict_new['fps'] = meta_dict['streams'][1]['avg_frame_rate']
    else:
        try:
            meta_dict_new['last'] = meta_dict['streams'][0]['nb_frames']
        except KeyError:
            duration = float(meta_dict['streams'][0]['duration'])
            fps_split = meta_dict['streams'][0]['avg_frame_rate'].split('/')
            avg_frame_rate = float(int(fps_split[0])/int(fps_split[1]))
            meta_dict_new['last'] = int(duration * avg_frame_rate) - 1
        meta_dict_new['fps'] = meta_dict['streams'][0]['avg_frame_rate']

    return meta_dict_new

def MakeSlateMOV(argv):

    ReadPath = argv[1]
    WritePath = argv[2]

    if ReadPath.split('.')[-1].lower() == 'r3d':
        with open('{}/utils/gizmos/Eleve_slate_RED.nk'.format(Eleve_root)) as f:
            tempNK = f.read()
    else:
        with open('{}/utils/gizmos/Eleve_slate.nk'.format(Eleve_root)) as f:
            tempNK = f.read()

    if ReadPath.split('.')[-1].lower() in ['mov', 'mp4', 'avi', 'r3d']:
        metadata_dict = query_metadata(ReadPath)
        first = metadata_dict['first']
        last = metadata_dict['last']
        if metadata_dict['fps']:
            fps = metadata_dict['fps']
        else:
            fps = "24"
    else:
        seq_model = fth_seq.find_seq(argv[1])
        first = seq_model['start']
        last = seq_model['end']
        fps = "24"

    WritePath_split = WritePath.split('/')
    Cilp_name = WritePath_split[-1].split('.')[0]
    Group_name = WritePath_split[5]
    Proxy_Path = '/'.join(WritePath_split[:5])
    ext = ReadPath.split('.')[-1]
    renderPath = os.path.join(Proxy_Path, 'tmp', Group_name)

    newNK = re.sub('info_orgSeq'     , ReadPath   , tempNK)
    newNK = re.sub('info_movfile'    , WritePath  , newNK)
    newNK = re.sub('info_startframe' , str(first) , newNK)
    newNK = re.sub('info_endframe'   , str(last)  , newNK)
    newNK = re.sub('info_fps', str(fps), newNK)

    color_rec709 = ['mov', 'mp4', 'tiff', 'tif', 'jpg', 'jpeg', 'png']
    if ext in color_rec709:
        newNK = re.sub('info_colorspace', 'Output - Rec.709', newNK)
    elif ext == 'dpx':
        newNK = re.sub('info_colorspace', 'Input - ARRI - V3 LogC (EI800) - Wide Gamut', newNK)
    elif ext == 'tga':
        newNK = re.sub('info_colorspace', 'Output - sRGB', newNK)
    else:
        newNK = re.sub('info_colorspace', 'ACES - ACEScg', newNK)

    ociotxt = 'defaultViewerLUT  "OCIO LUTs" \
    OCIO_config custom \
    customOCIOConfigPath /core/Linux/APPZ/ocio/RV_GLOBAL/config.ocio'
    newNK = re.sub('info_ocio', ociotxt , newNK)

    if 'Reference' in Group_name:
        newNK = re.sub('disable_slate', "true", newNK)
    else:
        newNK = re.sub('disable_slate', "false", newNK)

    if not os.path.isdir(renderPath):
        os.makedirs(renderPath)
    renderNK = os.path.join(renderPath, Cilp_name + '.nk')

    with open(renderNK, 'w') as f:
        f.write(newNK)
    f.close()

    return renderNK

if __name__ == '__main__':
    result=MakeSlateMOV(sys.argv)
    sys.exit(result)
