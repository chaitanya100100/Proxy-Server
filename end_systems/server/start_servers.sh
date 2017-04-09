#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage : bash $0 <SERVER_START_PORT> <SERVER_END_PORT>"
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
	screen -dm python server.py $i
done
