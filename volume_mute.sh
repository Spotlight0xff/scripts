amixer -q set Master toggle
mute=$(amixer -c 0 get Master | grep Mono: | grep -o -E '\[(on|off)\]')
if [[ "$mute" == "[off]" ]]; then
    volnoti-show -m
else
    vol=$(amixer -c 0 get Master | grep Mono: | cut -d " " -f6 | grep -o -E '[0-9]*')
    volnoti-show $vol
fi
