#!/bin/sh
CURDIR=`dirname $0`
width=$(xrandr | grep '*' | cut -d'x' -f1| tr -d '[[:space:]]')
if [[ $width == 1366 ]]; then
    file="$CURDIR/wallpaper-1107219_laptop.png"
else
    file="$CURDIR/wallpaper-1107219.png"
fi

i3lock -i $file
