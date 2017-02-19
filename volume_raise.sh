SINK=$(pactl list short | grep RUNNING | sed -e 's,^\([0-9][0-9]*\)[^0-9].*,\1,')

pactl set-sink-volume $SINK +5%
VOLUME=$(pactl list sinks | grep '^[[:space:]]Volume:' | \
  head -n $(( $SINK + 1 )) | tail -n 1 | sed -e 's,.* \([0-9][0-9]*\)%.*,\1,')
volnoti-show $VOLUME &
