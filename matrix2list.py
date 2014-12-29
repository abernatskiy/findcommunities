#!/usr/bin/python2

# Converts adjacency matrix to adjacency list
# Sets of input and output nodes are assumed to be the same

import sys

if len(sys.argv) != 1:
	raise ValueError("Use matrix2list.py by feeding it matrices through stdin and obtaining lists through stdout")

mline = sys.stdin.read()
vals = map(float, mline.split(' '))

import numpy as np
dim = np.sqrt(len(vals))

if not dim.is_integer():
	raise ValueError("Error: input matrix must be square")
dim = int(dim)
	
matrix = np.array(vals).reshape(dim, dim)
for i in xrange(dim):
	for j in xrange(dim):
		if matrix[i][j] != 0:
			print(str(i) + ' ' + str(j))
