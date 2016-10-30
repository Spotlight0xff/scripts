amixer -q -M set Master 5%+
vol=$(amixer get Master | grep Mono: | cut -d " " -f6 | grep -o -E '[0-9]*')
volnoti-show $vol
