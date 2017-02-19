#!/bin/bash

SINK=$(pactl list short | grep RUNNING | sed -e 's,^\([0-9][0-9]*\)[^0-9].*,\1,')
pactl set-sink-mute $SINK toggle

mute=$(pactl list sinks | grep -A15 -P "\#$SINK" | grep Mute | cut -d' ' -f2)
if [[ "$mute" == "yes" ]]; then
  volnoti-show -m
else
  VOLUME=$(pactl list sinks | grep '^[[:space:]]Volume:' | \
    head -n $(( $SINK + 1 )) | tail -n 1 | sed -e 's,.* \([0-9][0-9]*\)%.*,\1,')
  volnoti-show $VOLUME
fi
