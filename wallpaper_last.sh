#!/bin/sh
FILE=~/tmp/wallpapers
TMP=~/tmp/tmp_wallpapers

last=$(tail -2 $FILE | head -1)
if [ $? -eq 0 ]; then
    echo $last
    feh --bg-max "$last"
    head -n -1 $FILE > $TMP
    mv $TMP $FILE
fi

