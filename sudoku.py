#!/usr/bin/env python
from __future__ import division
import itertools, sys

defaultFileName = "sudoku.txt"

constraintTypes 	= { 
			0: [0, "row", "R", "r"],
			1: [1, "column", "C", "c"],
			2: [2, "block", "B", "b"]}


constraints = list(itertools.product(range(3), range(9)))

sudoku = [[{"a": range(1,10), "v": '-'} for x in xrange(9)] for x in xrange(9)] 

def s(c):
	i, j = c
	return sudoku[i][j]

def printInfoBlock(t, n):
	print "INFO CELLS", t, n, ":"
	for c in getFields(t, n):
		if s(c)["v"] == "-":
			print c, ":", s(c)

def printInfo(c):
	print "INFO CELL ", c, ":", s(c)

def printSudoku():
	for j in range(10):
		if j == 0:
			print "     0  1  2   3  4  5   6  7  8  "
		if j%3 == 0:
			print "   " + "---"*9 + "----"
		if j == 9:
			break;

		line = " "  + str(j) + " "

		for i in range(9):
			if i%3 == 0:
				line += "|"
			line += " " + str(s((j,i))["v"]) + " "
		line += "|"
		print line

def	cToStr(c, i = 2):
	t, n = c
	return constraintTypes[t][i] + str(n)

def export(fileName = defaultFileName):
	lines = []
	for j in range(9):
		line = ""
		for i in range(9):
			line += str(s((j,i))["v"])
		lines.append(line + "\n")
	with open(fileName, 'w') as f:
		f.writelines(lines)


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

def getFields(f, c = None):
	if c is None:
		f, c = f

	it = []
	if f in constraintTypes[0]:
		it = getRowIndexes(c)
	elif f in constraintTypes[1]:
		it = getColIndexes(c)
	elif f in constraintTypes[2]:
		it = getBlockIndexes(c)

	return it

def addValues(c, v):
	i, j = c
	s(c)["v"] = v
	s(c)["a"] = []
	for t in constraintTypes:
		for cc in getFields(t, c):
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
			
# Check if exists only one last possible value for a cell
def checkLast():
	for c in itertools.product(range(9), range(9)):
		if len(s(c)['a']) == 1:
			return (c, s(c)['a'][0], "LAST")

# Check std constraints
def checkOne():
	for c in constraints:
		for v in range(1, 10):
			t = []
			for field in getFields(c):
				if v in s(field)['a']:
					t.append(field)
			if len(t) == 1:
				return (t[0], v, c[0])
			

def clearTwo():
	for c in constraints:
		missing = 0
		for field in getFields(c):
			if s(field)['v'] == "-":
				missing += 1
		
		if missing == 0:
			continue

		p = {}
		p2 = {}
		p3 = []
		for v in range(1, 10):
			p2[v] = []
			for i, field in enumerate(getFields(c)):
				if v in s(field)['a']:
					if v not in p:
						p[v] = []
					p[v].append(field)
					p2[v].append(i)
					if i not in p3:
						p3.append(i)


		pl = {}

		print cToStr(c), "Missing:", missing
		print ' ',
		for f in p3:
			print f,
		print

		for v in p:
			print v, 
			for f in p3:
				if f in p2[v]:
					print 'x',
				else:
					print '-',
			print
		print

		for co in range(1, missing):
			temp = itertools.combinations(p3, co)
			for item in temp:
				j = 0
				for v in p:
					k = 0
					for ii in item:
						if ii not in p2[v]:
							k += 1
					if k == len(item):
						j +=1
				if j >= (missing - len(item)):
					print "yeah clustering", item
					print "sorry not implemented"
					print "do it yourself", constraintTypes[c[0]][1], c[1]


		for v in p:
			if len(p[v]) not in pl:
				pl[len(p[v])] = []

			#print "   - Value", v, ":", p[v]
			pl[len(p[v])].append({"v": v, "s": set(p[v])})


		for l in pl:
			if l > len(pl[l]):
				continue
			if l == missing:
				continue

			cSets = itertools.combinations(pl[l], l)
			#if  l > missing:

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


def clearOne():
	haveTo = {}
	for c in constraints:
		for v in range(1, 10):
			t = []
			for field in getFields(c):
				if v in s(field)['a']:
					t.append(field)
			if len(t) > 0:
				haveTo[(c, v)] = set(t)

	for c in constraints:
		fields = set(getFields(c))
		for entry in haveTo:
			cc, v = entry
			if cc != c:
				if fields.issuperset(haveTo[entry]):
					for field in fields:
						if field not in haveTo[entry]:
							if v in s(field)['a']:
								print "removing", v, "from", field, constraintTypes[c[0]][1], c[1], fields, haveTo[entry]
								s(field)['a'].remove(v)



fileName = defaultFileName
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
		if kIn == "s":
			printSudoku()
		if kIn == "q":
			exit()
		if kIn == "e":
			export()
		if len(kIn) == 2:
			f = kIn[0]
			j = int(kIn[1])
			try:
				i = int(f)
				printInfo((i, j))
			except ValueError:
				printInfoBlock(f,j)
			
	clearOne()
	clearTwo()
	info = checkOne()
	if info is None:
		info = checkLast()

	if info != None:
		c, v, t = info
		i, j = c
		print "Thats easy, look at the cell " + str(i) + ", " + str(j) + "!"
		if t != "LAST":
			print "Another hint, it's the", constraintTypes[t][1], "constraint."
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
			if checkOne():
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

	


