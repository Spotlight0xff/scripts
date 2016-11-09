#!/usr/bin/bash
focused_ws=$(i3-msg -t get_workspaces | jq '.[]|select(.focused == true).num')
i3-input -F "rename workspace to \"${focused_ws}: %s\"" -P 'New name: '
