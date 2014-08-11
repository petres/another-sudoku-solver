#!/usr/bin/env python
from __future__ import division
import itertools, sys

constraintTypes = ["row", "column", "block"]

sudoku = [[{"a": range(1,10), "v": '-'} for x in xrange(9)] for x in xrange(9)] 

def s(c):
	i, j = c
	return sudoku[i][j]

def printInfo(c):
	print "INFO CELL ", c
	print s(c)


def printSudoku():
	for j in range(10):
		if j == 0:
			print "    0  1  2   3  4  5   6  7  8  "
		if j%3 == 0:
			print "  " + "---"*9 + "----"
		if j == 9:
			break;

		line = str(j) + " "

		for i in range(9):
			if i%3 == 0:
				line += "|"
			line += " " + str(s((j,i))["v"]) + " "
		line += "|"
		print line

def getRowIndexes(c):
	if isinstance(c, tuple):
		i, j = c
	else:
		i = c
	return itertools.product([i], range(9))

def getColIndexes(c):
	if isinstance(c, tuple):
		i, j = c
	else:
		j = c
	return itertools.product(range(9), [j])

def getBlockIndexes(c):
	if isinstance(c, tuple):
		i, j = c
	else:
		i = c - c%3
		j = c%3 * 3
	ii = i%3
	jj = j%3
	return itertools.product(range(i - ii, i - ii + 3), range(j - jj, j - jj + 3))

def getIndexes(f, c):
	if f == "row":
		it = getRowIndexes(c)
	elif f == "column":
		it = getColIndexes(c)
	elif f == "block":
		it = getBlockIndexes(c)
	return it


def addValues(c, v):
	i, j = c
	s(c)["v"] = v
	s(c)["a"] = []
	for t in constraintTypes:
		for cc in getIndexes(t, c):
			ii, jj = cc
			if v in s(cc)["a"]:
				s(cc)["a"].remove(v)



def reading(fileName):
	with open(fileName, 'r') as sudokuFile:
		content = sudokuFile.read()

	for i in range(9):
		for j in range(9):
			value = content[j + i*(9+1)]
			if value != "-":
				value = int(value)
				addValues((i,j), value)
			


def checkOne(deep = False):
	for c in itertools.product(range(9), range(9)):
		if len(s(c)['a']) == 1:
			return (c, s(c)['a'][0], "LAST")

	deepFound = False
	for t in constraintTypes:
		for n in range(9):
			p = {}
			for v in range(1, 10):
				p[v] = []
				times = 0
				for c in getIndexes(t, n):
					if v in s(c)['a']:
						p[v].append(c)
			pl = {}
			for v in range(1, 10):
				if len(p[v]) == 1:
					if not deep:
						return (p[v][0], v, t)
				elif len(p[v]) > 1:
					if len(p[v]) not in pl:
						pl[len(p[v])] = []
					pl[len(p[v])].append({"v": v, "s": set(p[v])})
			if deep:
				for l in pl:
					if l > len(pl[l]):
						continue

					cSets = itertools.combinations(pl[l], l)

					for cSet in cSets:
						vs = []
						compareSet = None
						same = False
						for iSet in cSet:
							if compareSet is None:
								compareSet = iSet["s"]							
							if compareSet != iSet["s"]:
								same = False
								break
							same = True
							vs.append(iSet['v'])
					
						if same == True:
							toPrint = "Note that the cells "
							for c in compareSet:
								toPrint += str(c) + " "
								s(c)['a'] = list(vs)
							toPrint += "have to contain one of the values " + str(vs) + "."
							print toPrint
							deepFound = True
	if deep:
		return deepFound

fileName = "sudoku.txt"
if len(sys.argv) > 1:
	fileName = sys.argv[1]

reading(fileName)
printSudoku()


oldMissing = 81
missing = 100

it = 0
while(True):
	while True:
		kIn = raw_input("\nPress Enter to enter next round ... \n")
  		if len(kIn) == 0:
			break
		if len(kIn) == 3:
			exit()
		if len(kIn) == 2:
			i = int(kIn[0])
			j = int(kIn[1])
			printInfo((i, j))
	
	info = checkOne()

	if info != None:
		c, v, t = info
		i, j = c
		print "Thats easy, look at the cell " + str(i) + ", " + str(j) + "!"
		if t != "LAST":
			print "Another hint, it's the", t, "constraint."
		else:
			print "Maybe there is only one number left, which fits in this cell."

		#raw_input("\nPress Enter to enter next round ... \n")

		#print "Setting", i, j, "to", v, t
		addValues(c, v)
	else:
		if it == 0:
			print "No idea, seems to be a complex one!"
		else:
			print "Wait, lets look more detailed ... "
			if checkOne(True):
				it = 0
			else:
				print "Sorry, I give up!"
				exit()

	missing = 0
	for c in itertools.product(range(9), range(9)):
		i, j = c
		if sudoku[i][j]["v"] == "-":
			missing += 1

	print "\n\n"
	printSudoku()

	if missing == 0:
		print "Finished!!!"
		exit()

	if missing == oldMissing:
		it += 1
	oldMissing = missing

	


