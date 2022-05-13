#!/bin/sh

sourcefile="$1"
final_gif="$2"
ffprobe=/core/Linux/APPZ/packages/nuke_inhouse/1.0.0/python/Eleve/utils/ffmpeg/ffprobe
ffmpeg=/core/Linux/APPZ/packages/nuke_inhouse/1.0.0/python/Eleve/utils/ffmpeg/ffmpeg

# Overly simple validation
if [ ! -e "$sourcefile" ]; then
  echo 'Please provide an existing input file.'
  exit
fi

# Get video length in seconds
length=$($ffprobe "$sourcefile"  -show_format 2>&1 | sed -n 's/duration=//p' | awk '{print int($0)}')

# Start 20 seconds into the video to avoid opening credits (arbitrary)
starttimeseconds=0

# Mini-snippets will be 2 seconds in length
snippetlengthinseconds=2

# We'll aim for 5 snippets spread throughout the video
desiredsnippets=5

# Ensure the video is long enough to even bother previewing
minlength=$(($snippetlengthinseconds*$desiredsnippets))

# Video dimensions (these could probably be command line arguments)
dimensions=640:360

# Temporary directory and text file where we'll store snippets
# These will be cleaned up and removed when the preview image is generated
filename=$(basename -- "$sourcefile")
filename="${filename%.*}"
sourcefile_split=($(echo $sourcefile | tr "/" "\n"))
folder_group=${sourcefile_split[-3]}/${sourcefile_split[-2]}/$filename
tempdir=/core/TD/Eleve/Proxy/Reference/$folder_group
listfile=/core/TD/Eleve/Proxy/Reference/$folder_group.txt
destfile=/core/TD/Eleve/Proxy/Reference/$folder_group.mov

# Display and check video length
echo 'Video length: ' $length
if [ "$length" -lt "$minlength" ]
then
  echo 'Video is too short.'
  $ffmpeg -y -i $sourcefile -vf scale=250:180:force_original_aspect_ratio=decrease -r 24 $final_gif -hide_banner
  exit
fi

# Loop and generate video snippets
if [ ! -d $tempdir ]; then
  mkdir -p $tempdir
fi
interval=$(($length/$desiredsnippets-$starttimeseconds))
for i in $(seq 1 $desiredsnippets)
  do
    # Format the second marks into hh:mm:ss format
    start=$(($(($i*$interval))+$starttimeseconds))
    formattedstart=$(printf "%02d:%02d:%02d\n" $(($start/3600)) $(($start%3600/60)) $(($start%60)))
    echo 'Generating preview part ' $i $formattedstart
    # Generate the snippet at calculated time
    #$ffmpeg -ss $formattedstart -t $snippetlengthinseconds -i $sourcefile -vf scale=$dimensions -preset fast -qmin 1 -qmax 1 $tempdir/$i.mov &>/dev/null
    $ffmpeg -ss $formattedstart -t $snippetlengthinseconds -i $sourcefile -vf scale=$dimensions -preset fast -qmin 1 -qmax 1 $tempdir/$i.mov &>/dev/null
done

# Concat videos
echo 'Generating final preview file'

# Generate a text file with one snippet video location per line
# (https://trac.ffmpeg.org/wiki/Concatenate)
for f in $tempdir/*; do echo "file '$f'" >> $listfile; done

# Concatenate the files based on the generated list
$ffmpeg -y -f concat -safe 0 -i $listfile -c copy $destfile

# Cleanup
rm -rf $tempdir $listfile


# Final Convert mov to gif
$ffmpeg -y -i $destfile -vf scale=250:180:force_original_aspect_ratio=decrease -r 24 $final_gif -hide_banner
