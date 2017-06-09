#!/usr/bin/bash
WALLPATH=~/cloud/Photos/Wallpaper/


while true; do
    tail -n 200 ~/tmp/wallpapers > ~/tmp/wallpapers_tmp
    cat ~/tmp/wallpapers_tmp > ~/tmp/wallpapers
    rm ~/tmp/wallpaper_tmp
    name=$(find $WALLPATH -type f \( -name '*.jpeg' -o -name '*.png' -o -name '*.jpg' \) -print0 | shuf -n1 -z)
    echo $name >> ~/tmp/wallpapers
    feh --bg-max "$name"
    sleep 30s
done
