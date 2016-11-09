amixer -q -M set Master 5%-
#vol=$(amixer get Master | grep Mono: | cut -d " " -f6 | grep -o -E '[0-9]*')
vol=$(amixer get Master | grep -m1 -o "[0-9]*\%" | grep -o "[0-9]*")
volnoti-show $vol
