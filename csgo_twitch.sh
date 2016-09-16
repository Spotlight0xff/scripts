#!/bin/bash

CONFIG_FILE="/home/$USER/.config/scripts/streams.ini"
MY_PATH="`dirname \"$0\"`"

(streams=$(python2 $MY_PATH/streams.py -f "$CONFIG_FILE" -d '`')
echo "$streams" > /tmp/.streams
) | zenity --progress --pulsate --auto-close --text="Fetch CS:GO Streams"

if [ $? == 1 ] ; then exit; fi

i=-1
while read line;
do
    i=$(($i+1))
    name=$(echo $line | cut -d '`' -f1)
    viewers=$(echo $line | cut -d '`' -f2)
    array[$i]=$(echo "$name $viewers")
done < /tmp/.streams

rm /tmp/.streams

sel=$(zenity --list --title="Choose the Livestream" \
    --column="Name" --column="Viewers"\
    ${array[*]})
if [ ! $sel ]; then exit; fi
$MY_PATH/twitch.sh $sel

