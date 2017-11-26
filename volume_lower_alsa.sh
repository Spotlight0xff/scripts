#!/bin/bash
amixer set Master 5%-
VOLUME=$(awk -F"[][]" '{ print $2 }' <(amixer sget Master) | tail -1)
volnoti-show $VOLUME &
