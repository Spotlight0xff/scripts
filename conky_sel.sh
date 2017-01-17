#!/usr/bin/bash

width=$(xrandr | grep '*' | cut -d'x' -f1| head -1 |tr -d '[[:space:]]')

if [[ $width == 1366 ]]; then
    dir="laptop"
elif [[ $width == 1280 ]]; then
    dir="1024"
else
    dir="fullhd"
fi

conky -c ~/.conky/$dir/conky_overlay.conf &
conky -c ~/.conky/$dir/conky_bar.conf &
