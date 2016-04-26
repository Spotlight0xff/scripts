#!/bin/sh
current_now=$(cat /sys/class/power_supply/BAT0/current_now)
voltage_now=$(cat /sys/class/power_supply/BAT0/voltage_now)

echo $(bc <<< "scale=1;($current_now * $voltage_now) / 1000000000000")
