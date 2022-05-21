import os

config = {}

config['ADMIN'] = ['gisub']
config['LEADER'] = []
for a in config['ADMIN']:
    config['LEADER'].append(a)
config['SEMI_LEADER'] = []
for a in config['LEADER']:
    config['SEMI_LEADER'].append(a)

config['NAME'] = 'Eleve'
Eleve_root = '/core/Linux/APPZ/packages/nuke_inhouse/1.0.0/python/{0}'.format(config['NAME'])
Eleve_element = '/core/TD/{0}'.format(config['NAME'])

config['icons'] = '{0}/icons'.format(Eleve_root)
config['gizmos'] = '{0}/utils/gizmos'.format(Eleve_root)

config['ffmpeg'] = '{0}/utils/ffmpeg'.format(Eleve_element)
config['proxy'] = '{0}/Proxy'.format(Eleve_element)
config['alftmp'] = '{0}/tmp'.format(config['proxy'])
config['reference'] = '/m83_lib/2D_source_collect/Reference'
config['json'] = '{0}/preference/data.json'.format(Eleve_element)

config['PATH_PERSONAL_CONFIG'] = "{0}/.config/{1}/personal-config.json".format(os.environ['HOME'], config['NAME'])
config['fav_data'] = "{0}/.config/{1}/fav_data.json".format(os.environ['HOME'], config['NAME'])

config['threads'] = '4'
config['img_seq'] = 'True'
config['DIMENSION_X'] = 250
config['DIMENSION_Y'] = 180

config['spool'] = '/core/Linux/APPZ/renderFam/tractor/pixar/Tractor-2.2/bin/tractor-spool'
