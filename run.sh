#! /bin/bash

if [ ! -d "./output" ]; then
  mkdir ./output
fi

python wav_to_h5.py
python beamform.py
python merge_videos.py
