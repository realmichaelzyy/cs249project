#!/bin/bash

# Extracts all XML files for a given year
# Invokes the abstractor script
# Cleans up after itself

rm *.xml > /dev/null
rm *.pkl > /dev/null

for year in {1976..2014}
do
	unzip $year.zip > /dev/null
	echo 'Invoking abstractor for year' $year
	fname='df-'$year'.msg'
	python abstractor5.py $fname >> invokelog.txt
	rm *.xml > /dev/null
done
