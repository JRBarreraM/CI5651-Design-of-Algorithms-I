import sys

if len(sys.argv) < 3:
    print("No se indico ningun archivo")
    sys.exit()
fileName1 = sys.argv[1]
fileName2 = sys.argv[2]

# Opens the file
try:
    data1=open(fileName1, "r")
    data2=open(fileName2, "r")
except:
    print("No se pudo abrir el archivo")
    sys.exit()

lines1 = data1.readlines()
lines2 = data2.readlines()
data1.close()
data2.close()

k = 1
for i in range(len(lines1)):
    print("Instacia: " + str(k))
    print()
        
    orden = int(lines1[i].split()[0])
    sudoku1 = lines1[i].split()[1]
    temp = lines2[i]
    if not ((temp[0] == 'I') or (temp[0] == 'N')):
        sudoku1 = [int(x) for x in sudoku1]
        sudoku2 = [int(x) for x in temp.split()[1]]

        for i in range(0, len(sudoku1), orden**2):
            if (i == 4*orden**2):
                print(str(sudoku1[i:i+orden**2]) + " --> " + str(sudoku2[i:i+orden**2]))
            else:
                print(str(sudoku1[i:i+orden**2]) + "     " + str(sudoku2[i:i+orden**2]))
        print()
        k += 1
    else:
        sudoku1 = lines1[i].split()[1]
        sudoku1 = [int(x) for x in sudoku1]

        for i in range(0, len(sudoku1), orden**2):
            if (i == 4*orden**2):
                print(str(sudoku1[i:i+orden**2]) + " --> " + str(temp[:-1]))
            else:
                print(str(sudoku1[i:i+orden**2]))
        print()
        k += 1