#!/bin/bash


keys=('read' 'len' 'columns' 'dtypes')

for key in "${keys[@]}"
do
	if [ $key == 'read' ] && [ $1 == $key ]
        then
		curl -X 'GET' 'http://0.0.0.0:8000/data/read/?name='$2'&separator=%3B' -H 'accept: application/json'
	elif [ $1 == $key ]
        then
		curl -X 'GET' 'http://0.0.0.0:8000/data/'$1'/' -H 'accept: application/json'
	fi
done
