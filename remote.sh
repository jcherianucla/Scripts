#!/bin/bash

while true; do
	COMP_NAME="jahan_mac_pro_ret"

	if [[ ! -d $HOME"/Dropbox/IP/" ]]; then
		mkdir $HOME"/Dropbox/IP/"
	fi

	if [[ ! -f $HOME"/Dropbox/IP/"$COMP_NAME ]]; then
		touch $HOME"/Dropbox/IP/"$COMP_NAME
	fi

	OLD_IP=$(<$HOME"/Dropbox/IP/"$COMP_NAME)

	NEW_IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -n 1)

	if [[ "$NEW_IP" != "$OLD_IP" ]]; then
		echo "$NEW_IP" > "$HOME""/Dropbox/IP/""$COMP_NAME"
	fi
	
	sleep 60
done
