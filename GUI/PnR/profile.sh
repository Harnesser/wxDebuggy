#!/usr/bin/env sh

module='ga'

mkdir logs
svn_rev=`svn info ./${module}.py | grep Revision | cut -d" " -f2`

logfile_name="${module}:`date +"%F___%X\"`___Rev${svn_rev}.log"
python -m cProfile -s 'time' ./${module}.py | tee  ./logs/${logfile_name}

exit

