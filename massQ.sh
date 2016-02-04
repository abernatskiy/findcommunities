#!/bin/bash

# Parsing CLI and taking care of help

TEMP=`getopt -o i:o:h: --long help,input:,output:,hidden: -- "$@"`
eval set -- "$TEMP"

function printUsage {
cat << EOF

Usage: massQ.sh [<txtpipe> <binpipe>] [-i|--input inputNodes -o|--output outputNodes [-h|--hidden hiddenNodes]]

Takes network genomes in evs format as its standard input, produces a modularity score and writes it into
the standard output. Network topology is given by -i,-o and -h parameter; if no parameters are given,
the self-connected topology is assumed.
To work, must be located at ~/findcommunities/massQ.sh.
Requires two named pipes to work - one for intermediate text formst and one for intermediate binary format.
Unless explicitly specified, will use "./txt" and "./bin".
EOF
}

while true; do
	case $1 in
		--help)
			printUsage; exit 1; shift;;
		-i|--input)
			INPUTN="$2"; shift 2;;
		-o|--output)
			OUTPUTN="$2"; shift 2;;
		-h|--hidden)
			HIDDENN="$2"; shift 2;;
		--) shift; break;;
		*) echo "Internal error!" ; exit 1;;
	esac
done

if { [ -z "$INPUTN" ] && [ ! -z "$OUTPUTN" ]; } || { [ ! -z "$INPUTN" ] && [ -z "$OUTPUTN" ]; } ; then
	echo "-i|--input and -o|--output options must be always used together";
	exit 1;
fi

if [ ! -z "$HIDDENN" ] && [ -z "$INPUTN" ] ; then
	echo "-h|--hidden must always be used with -i|--input and -o|--output";
	exit 1;
fi

GTOLCLARGS=`echo "$INPUTN $OUTPUTN $HIDDENN" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'`

# The program itself

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

FINDCOMMUNITIES_DIR="${HOME}/findcommunities"
COMMDIR="${FINDCOMMUNITIES_DIR}/Community_latest/"
COMMCONV="${COMMDIR}convert"
COMMCOMM="${COMMDIR}community"
GTOL="${FINDCOMMUNITIES_DIR}/genome2list.py"

IFS=$'\n'
for line in `cat`; do
	ID=`echo ${line} | cut -d ' ' -f 1`
	MATRIXSTR=`echo ${line} | cut -d ' ' -f 2-`
	echo $MATRIXSTR | python $GTOL $INPUTN $OUTPUTN $HIDDENN > $TXT &
	$COMMCONV -i $TXT -o $BIN &
	QVAL=`$COMMCOMM $BIN -l -1 -v 2>&1 | tail -1`
	if [ "$QVAL" == "Begin:" ]; then
		QVAL=0
	fi
	echo $ID $QVAL
done
