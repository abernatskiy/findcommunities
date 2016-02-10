#!/usr/bin/python2

# Converts adjacency matrix to adjacency list
# Sets of input and output nodes are assumed to be the same

import argparse
import numpy as np
import sys

def printMatrixAsList(matArr, N, M, firstNode=0, sameNodes=False, useWeights=False):
	matrix = np.array(matArr).reshape(N, M)
	for i in xrange(N):
		for j in xrange(M):
			if matrix[i][j] != 0:
				if sameNodes:
					fromNode = firstNode + i
					toNode = firstNode + j
				else:
					fromNode = firstNode + i
					toNode = firstNode + N + j
				if useWeights:
					print(str(fromNode) + ' ' + str(toNode) + ' ' + str(matrix[i][j]))
				else:
					print(str(fromNode) + ' ' + str(toNode))

def printSelfConnectedGraph(vals, useWeights=False):
	dim = np.sqrt(len(vals))
	if not dim.is_integer():
		raise ValueError('Error: input matrix must be square')
	dim = int(dim)
	printMatrixAsList(vals, dim, dim, sameNodes=True, useWeights=useWeights)

def printInputOutputGraph(vals, inNodes, outNodes, useWeights=False):
	if len(vals) != inNodes*outNodes:
		raise ValueError('Error: wrong input size for the specified dimensions (' + str(len(vals)) + '!=' + str(inNodes) + '*' + str(outNodes) + ')')
	printMatrixAsList(vals, inNodes, outNodes, useWeights=useWeights)

def printInputHiddenOutputGraph(vals, inNodes, outNodes, hiddenNodes, useWeights=False, recurrentHidden=False):
	requiredVals = inNodes*hiddenNodes + hiddenNodes*outNodes
	requiredVals += hiddenNodes*hiddenNodes if recurrentHidden else 0
	if len(vals) != requiredVals:
		errorStr = 'Error: wrong input size for the specified dimensions (' + str(len(vals)) + '!=' + str(inNodes) + '*' + str(hiddenNodes) + ' + ' + str(hiddenNodes) + '*' + str(outNodes)
		errorStr += '+' + str(hiddenNodes) + '*' + str(hiddenNodes) + ')' if recurrentHidden else ')'
		raise ValueError("Error: wrong input size for the specified dimensions (" + str(len(vals)) + "!=" + str(inNodes) + '*' + str(hiddenNodes) + ' + ' + str(hiddenNodes) + '*' + str(outNodes) + ')')

	curWtsSt = 0
	curNodeSt = 0

	printMatrixAsList(vals[curWtsSt:curWtsSt+inNodes*hiddenNodes], inNodes, hiddenNodes, firstNode=curNodeSt, useWeights=useWeights)
	curWtsSt = inNodes*hiddenNodes
	curNodeSt = inNodes

	if recurrentHidden:
		printMatrixAsList(vals[curWtsSt:curWtsSt+hiddenNodes*hiddenNodes], hiddenNodes, hiddenNodes, firstNode=curNodeSt, sameNodes=True, useWeights=useWeights)
		curWtsSt += hiddenNodes*hiddenNodes

	printMatrixAsList(vals[curWtsSt:], hiddenNodes, outNodes, firstNode=curNodeSt, useWeights=useWeights)

cliParser = argparse.ArgumentParser(description='genome2list.py - converiting serialized connectivity matrices to adjecency lists since 2015',
																		epilog='Use the program by piping the genomes into its stdin and getting adjacency lists out of stdout.'
																						'Don\'t use any arguments if your network\'s inputs coincide with its outputs (e.g. if it is a boolean network).\n'
																						'Always use inNodes and outNodes together.')
cliParser.add_argument('inNodes', metavar='inNodes', nargs='?', default=None, type=int, help='number of input nodes')
cliParser.add_argument('outNodes', metavar='outNodes', nargs='?', default=None, type=int, help='number of output nodes')
cliParser.add_argument('hiddenNodes', metavar='hiddenNodes', nargs='?', default=None, type=int, help='number of hidden nodes, negative means recursive')
cliParser.add_argument('-w', action='store_true', help='output a weighted graph')

args = cliParser.parse_args()
if args.inNodes is not None and args.outNodes is None:
	cliParser.error('If you indicate the number of input nodes, please also indicate the number of output nodes')

#print str(args.inNodes) + ' ' + str(args.outNodes) + ' ' + str(args.hiddenNodes)

mline = sys.stdin.read()
weights = map(float, mline.split(' '))
if args.inNodes is None and args.outNodes is None:
	printSelfConnectedGraph(weights, useWeights=args.w)
elif args.hiddenNodes is None:
	printInputOutputGraph(weights, args.inNodes, args.outNodes, useWeights=args.w)
else:
	absHiddenNodes = args.hiddenNodes if args.hiddenNodes > 0 else -1*args.hiddenNodes
	printInputHiddenOutputGraph(weights, args.inNodes, args.outNodes, absHiddenNodes, useWeights=args.w, recurrentHidden=(args.hiddenNodes<0))
