#!/bin/bash
#$1: <inputfile>, $2:X, $3: -apriori/-fptree, $4: <outputfilename>
if [ "$3" = "-apriori" ] ; then
	java Test $1 $2 $3 $4 > $4
elif [ "$3" = "-fptree" ]; then
 	java Test $1 $2 $3 $4 > $4
elif  [ "$2" = "-plot" ] ; then
	python3 plot.py $1
else
	echo "Argument is not valid!"
fi
