import sys

if len(sys.argv) < 2:
    print("No se indico ningun archivo")
    sys.exit()
fileName=sys.argv[1]

# Opens the file
try:
    data=open(fileName, "r")
except:
    print("No se pudo abrir el archivo")
    sys.exit()

lines = data.readlines()
data.close()

k = 1
for line in lines:
    print(k)
    sudoku = line.split()[1]
    sudoku = [int(x) for x in sudoku]
    for i in range(0, len(sudoku), 9):
        if (i == 4*9):
            print(str(sudoku[i:i+9]) + " = Salida")
        else:
            print(sudoku[i:i+9])
    print()
    k += 1
#te fuiste

#numbers = [ int(x) for x in numbers ]
