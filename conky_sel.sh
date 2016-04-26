#!/usr/bin/bash

width=$(xrandr | grep '*' | cut -d'x' -f1| tr -d '[[:space:]]')

if [[ $width == 1366 ]]; then
    dir="laptop"
else
    dir="fullhd"
fi
conky -c ~/.conky/$dir/conky_overlay.conf &
conky -c ~/.conky/$dir/conky_bar.conf &
