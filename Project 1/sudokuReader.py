import sys
import numpy as np
#Lector de Sudoku
# Give the lexer some input
if len(sys.argv) < 2:
    print("No file specified")
    sys.exit()
fileName=sys.argv[1]

# Opens the file
try:
    data=open(fileName, "r")
except:
    print("Error can't open file")
    sys.exit()

lines = data.readlines()
#sudoku = np.zeros(81)
sudoku = np.zeros((9,9))
k = 0
for line in lines:
    k += 1
    for i in range(81):
        sudoku[(i//9),(i%9)] = line[i+2]
    print("sudoku #%d" % (k))
    print(sudoku)
    print()