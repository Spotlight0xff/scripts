#!/bin/sh
brightness=$(xbacklight -get)
brightness=$(bc <<< "$brightness - 5")
volnoti-show -i monitor $brightness
xbacklight -5
