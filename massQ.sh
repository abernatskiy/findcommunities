#!/bin/bash

# Usage:
# massQ.sh [<txtpipe> <binpipe>]
# Takes network genomes in evs format as its standard input, produces a modularity score and writes it into
# the standard output.
# Must be run at the findcommunities directory.
# Requires two named pipes to work - one for intermediate text formst and one for intermediate binary format.
# Unless explicitly specified, will use "./txt" and "./bin" for these purposes.o

if [ $# -eq 2 ]; then
	TXT="$1"
	BIN="$2"
elif [ $# -eq 0 ]; then
	TXT="./txt"
	BIN="./bin"
else
  echo Wrong number of arguments
  exit 1
fi

COMMDIR="./Community_latest/"
COMMCONV="${COMMDIR}convert"
COMMCOMM="${COMMDIR}community"

IFS=$'\n'
for line in `cat`; do
	ID=`echo ${line} | cut -d ' ' -f 1`
	MATRIXSTR=`echo ${line} | cut -d ' ' -f 2-`
	echo $MATRIXSTR | python ./matrix2list.py > $TXT &
	$COMMCONV -i $TXT -o $BIN &
	QVAL=`$COMMCOMM $BIN -l -1 -v 2>&1 | tail -1`
	if [ "$QVAL" == "Begin:" ]; then
		QVAL=0
	fi
	echo $ID $QVAL
done
