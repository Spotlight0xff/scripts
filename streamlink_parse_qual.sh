#!/bin/bash

username=$1


output=$(streamlink twitch.tv/$username)

if [[ "$output" == *"source (best, worst)"* ]]; then
  qualities[0]="source"
  qual_count=0
else
  qual_count=$(echo $output|grep -o "," | wc -l)
  let qual_count=qual_count+1
fi
for ((i=1; i <= $qual_count; i++))
do
  qualities[$i]=$(echo $output| cut -d':' -f2| cut -d',' -f $i|cut -d' ' -f2)
done

printf "%s\n" "${qualities[@]}"
