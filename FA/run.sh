#!/bin/bash

mfa align --clean ./input spanish_latin_america_mfa spanish_mfa ./output

CWD=$(pwd)
LIST_NAME='Lista_A'

OUT=$(python3 $CWD/textgrid/textgrid.py -o $CWD/output/textgrid.csv $CWD/output/$LIST_NAME.TextGrid)

TIMESTAMPS=$(python3 return_timestamps.py $OUT)

AUDIO=$CWD/input/Lista_A.wav
AUDIO_OUT=$CWD/trimmed_audios

python3 trim_audio.py $TIMESTAMPS $AUDIO $AUDIO_OUT $LIST_NAME