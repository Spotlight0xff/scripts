#!/usr/bin/bash
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

        (output=$(livestreamer twitch.tv/$username)
        echo $output > /tmp/livestream_info
        )| zenity --progress --pulsate --auto-close --text="Fetch Livestream information"
        if [ $? == 1 ]; then exit; fi
        output=$(cat /tmp/livestream_info)

        if [[ "$output" == *"source (best, worst)"* ]]; then
            qualities[0]="source"
            qual_count=0
        else
            qual_count=$(echo $output|grep -o "," | wc -l)
            let qual_count=qual_count+1
        fi
        for ((i=1; i <= $qual_count; i++))
        do
            qualities[$i]=$(echo $output| cut -d':' -f2| cut -d',' -f $i|cut -d' ' -f2)
        done

        in=$(printf "%s\n" "${qualities[@]}" | rofi -dmenu p "quality")
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
