#!/bin/sh
CURDIR=`dirname $0`
FILE="$CURDIR/lock.png"
BACKGROUND="355C7D"
swaylock --indicator-radius 50 --indicator-thickness 4 --insidecolor $BACKGROUND --keyhlcolor 000000 --linecolor $BACKGROUND --ringcolor ${BACKGROUND}00 -r -t -i $FILE
