#!/bin/zsh

layouts=("English (us)" "German (de)")

output=$(echo "${(j:\n:)layouts}" | rofi -dmenu -p "Layout switch: ")

echo $output


case $output in
  "English (us)")
    setxkbmap us
    ;;

  "German (de)")
    setxkbmap de
    ;;
esac
