#!/bin/bash

screen -ls | grep Detached | cut -d "." -f 1 | while read pid; do
    echo $pid
	    screen -S $pid -X stuff ^C
		done

