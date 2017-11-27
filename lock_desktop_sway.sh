#!/bin/sh
CURDIR=`dirname $0`
file="$CURDIR/lock.png"

#swaylock --indicator-radius 50 --indicator-thickness 2 --insidecolor 80808080 --keyhlcolor 000000a0 --linecolor 80808080 --ringcolor 80808000 -r -t -i $file
swaylock --indicator-radius 50 --indicator-thickness 2 --insidecolor a0a0a0 --keyhlcolor 000000 --linecolor a0a0a0 --ringcolor a0a0a000 -r -t -i $file
