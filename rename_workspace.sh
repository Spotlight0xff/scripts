#!/usr/bin/bash
focused_ws=$(i3-msg -t get_workspaces | jq '.[]|select(.focused == true).num')
name=$(~/scripts/dpass.sh "Workspace: ")
if [ -z $name ];then
  i3-msg "rename workspace to \"${focused_ws}\""
  exit
fi
i3-msg "rename workspace to \"${focused_ws}: ${name}\""

