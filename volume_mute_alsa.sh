#!/bin/bash
amixer set Master toggle
VOLUME=$(awk -F"[][]" '{ print $2 }' <(amixer sget Master) | tail -1)
if amixer get Master | grep -q off; then
  volnoti-show -m
else
  volnoti-show $VOLUME &
fi
