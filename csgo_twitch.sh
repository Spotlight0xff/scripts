#!/bin/bash

CONFIG_FILE="/home/$USER/.config/scripts/streams.ini"
MY_PATH="`dirname \"$0\"`"

sel=$(python2 $MY_PATH/streams.py -f "$CONFIG_FILE" | column -s \| -t | rofi -dmenu -i -p "twitch.tv/" | cut -f1 -d' ')

if [ ! $sel ]; then exit; fi

$MY_PATH/twitch.sh $sel
