#!/bin/bash

if [ $# -ne 5 ]
then
	echo "Usage : bash $0 <CLIENT_START_PORT> <CLIENT_END_PORT> <PROXY_PORT> <SERVER_START_PORT> <SERVER_END_PORT>"
	exit
fi

re='^[0-9]+$'

for num in $@
do
	if ! [[ $num =~ $re ]] ; then
   		echo "error: Not a number $num"
		exit
	fi
done


for i in $(seq $1 $2)
do
	screen -dm python client.py $i $3 $(($4 + RANDOM % ($5 - $4 + 1)))
done
