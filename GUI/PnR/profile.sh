#!/usr/bin/env sh

mkdir logs
logfile_name=`date +"%F___%X.log"`
python -m cProfile -s 'time' ./ga.py | tee  ./logs/${logfile_name}

exit

