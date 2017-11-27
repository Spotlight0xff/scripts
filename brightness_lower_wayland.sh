#!/bin/sh
brightnessctl set 5%-
value=$(brightnessctl -m | cut -d',' -f4)
volnoti-show -s /usr/share/pixmaps/volnoti/display-brightness-symbolic.svg $value
