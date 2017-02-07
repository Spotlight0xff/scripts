#!/usr/bin/bash

scrot '%Y-%m-%d_$wx$h_scrot.png' -e 'mv --backup=t $f /home/spotlight/nextcloud/Photos/Screenshots/'
notify-send "Screenshot taken"
