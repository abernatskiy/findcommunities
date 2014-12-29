#!/bin/bash

IN="./in"
TXT="./txt"
BIN="./bin"
OUT="./out"

COMMDIR="./Community_latest/"
COMMCONV="${COMMDIR}convert"
COMMCOMM="${COMMDIR}community"

IFS=$'\n'
for line in `cat $IN`; do
	ID=`echo ${line} | cut -d ' ' -f 1`
	MATRIXSTR=`echo ${line} | cut -d ' ' -f 2-`
	echo $MATRIXSTR | ./matrix2list.py > $TXT &
	$COMMCONV -i $TXT -o $BIN &
	QVAL=`$COMMCOMM $BIN -l -1 -v 2>&1 | tail -1`
	echo $ID $QVAL
done
