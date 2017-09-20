#!/usr/bin/bash

MY_PATH="`dirname \"$0\"`"

if [[ ! $1 ]]; then
  echo "provide a twitch stream name!"
  exit
fi

username="$1"

in=$($MY_PATH/streamlink_parse_qual.sh $username| rofi -dmenu -p "Quality: ")
if [[ ! $in ]]; then exit; fi

streamlink -Q de.twitch.tv/$username $in
