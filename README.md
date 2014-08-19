### Sudoku Solver

This simple python script allows to solve Sudokus. It doesn't use any evolved technique, instead it tries to solve the sudoku like an human. Therefore each solution step can and will be explained. 

It can not solve all solveable Sudokus.


### Running

Before starting the algorithm the Sudoku has to be saved in an file like this:

```
----792-4
---1-----
-2----91-
--4-8-6-1
-8-----9-
3-6-1-5--
-47----8-
-----7---
1-386----
```

Afterwards the program has to be started by:
```
./sudoku.py sudokuFileName
```

Between each solving step you can interact with the program:
- `31` will print the info of cell 3, 1.
- `e` will export the Sudoku to sudoku.txt.
- `b1` will print the info of all cells in the second block. Works also with columns (c) and rows (r).
- `q` will quit the program. 
