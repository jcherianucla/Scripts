#!/bin/bash
SITES=("www.facebook.com")
HOST="/etc/hosts"
F_SITES=$SITES
IFS=", "

if [ ! -w $HOST ]; then
	echo "$HOST requires admin privilige. Please run script with sudo."
	exit 1
fi

read -n1 -p "Do you wish to work or play? [W/P] " decision

if [[ $decision == "W" || $decision == "w" ]]; then
	echo -e "\n"
	read -ep $"The blocked sites list is: ${SITES[@]}. Do you wish to add to this? [Y/N] " append
	if [[ $append == "Y" || $append == "y" ]]; then
		echo -e "Please enter the websites you want to add to the list: "
		read -a A_SITES 
		F_SITES=("${SITES[@]}" "${A_SITES[@]}") 
	fi
	for SITE in ${F_SITES[@]}; do
		echo -e "127.0.0.1\t$SITE\t#block" >> $HOST
	done
	echo -e "\n${F_SITES[@]} have been blocked. Run with P to use again."
	echo "Close the instances of the site in your browser for it to take effect."
	exit 1
else
	sed -i -e '/#block$/d' $HOST
	echo -e "\n${F_SITES[@]} have been unblocked. Run with W to block."
	exit 1
fi
