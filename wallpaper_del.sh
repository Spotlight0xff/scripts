#!/usr/bin/bash

if [[ -a ~/tmp/wallpapers ]]; then
    file=$(tail -1 ~/tmp/wallpapers)
    name=${file##*/}
    if zenity --question --text="Dude, delete that wallpaper '$name'? :/" ]]; then
        echo "del $file"
        rm "$file"
        ~/bin/wallpaper.sh
    fi
fi

