#!/usr/bin/bash

MY_PATH="`dirname \"$0\"`"

if [[ $1 ]]; then
    username=$1
else
    username=$(zenity --entry --title="Watch Twitchstreams" --text="Enter the Twitch.tv-Stream:")
    if [ ! $username ]; then exit; fi
fi

same_qual=false

while true
do
    if [ $same_qual == false ]; then
      in=$($MY_PATH/livestreamer_parse_qual.sh $username| rofi -dmenu -p "Quality: ")
      if [ ! $in ]; then exit; fi
    fi

    livestreamer -Q de.twitch.tv/$username $in

#    rr=$(zenity --question --text "Restart Stream?")
    if ! zenity --question --title=" " --text="Restart Stream?"; then
        break
    fi

 #   rr_qual=$(zenity --question --text "Same Quality?")
    if zenity --question --title="   " --text="Same Quality?"; then
        same_qual=true
    else
        same_qual=false
    fi
done
