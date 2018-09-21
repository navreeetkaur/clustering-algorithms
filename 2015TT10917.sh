#!/bin/bash
if [ "$1" = "-kmeans" ]; then
	python3 kmeans.py $2 $3
elif [ "$1" = "-dbscan" ]; then
 	./dbscan $2 $3 $4
elif [ "$1" = "-optics" ]; then
	python3 optics.py $4 $3 $2
else
	echo "Invalid arguments"
fi
