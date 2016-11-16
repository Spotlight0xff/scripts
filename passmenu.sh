#!/usr/bin/env bash

shopt -s nullglob globstar

typeit=0
if [[ $1 == "--type" ]]; then
	typeit=1
	shift
fi

prefix=${PASSWORD_STORE_DIR-~/.password-store}
password_files=( "$prefix"/**/*.gpg )
password_files=( "${password_files[@]#"$prefix"/}" )
password_files=( "${password_files[@]%.gpg}" )

if [[ $typeit -eq 1 ]]; then
  prompt='Type: '
else
  prompt='Show: '
fi

password=$(printf '%s\n' "${password_files[@]}" | dmenu "$@" -p "${prompt}")

[[ -n $password ]] || exit

if [[ $typeit -eq 0 ]]; then
  pwd=$(pass show "$password" 2>/dev/null)
  choosen=$(printf '%s\n' "${pwd}" | dmenu -p "Choose: ") 
  printf '%s\n' $choosen
else
	xdotool - <<<"type --clearmodifiers -- $(pass show "$password" | head -n 1)"
fi
