import sys

if len(sys.argv) < 2:
    print("No file specified")
    sys.exit()
fileName=sys.argv[1]

try:
    data=open(fileName, "r")
except:
    print("Error can't open file")
    sys.exit()

lines = data.readlines()
data.close()

line =  lines[0].split()
orden = int(line[0])
sudoku = [ [ 0 for i in range(orden**2) ] for j in range(orden**2) ]
variablesFijas = []
for i in range(orden**4):
    var = int(line[1][i])
    sudoku[(i//orden**2)][(i%(orden**2))] = var
    if var != 0:
        variablesFijas.append(i * orden**2 + var)

numOfClausulas = len(variablesFijas) + (orden**4) + ((orden**8 - orden**6) // 2) + (3 * (orden**8 - orden**6) // 2)

cnfSAT = "p cnf %d %d\n" % (int(orden**6), numOfClausulas)

#Clausulas de Variables Fijas
for var in variablesFijas:
    cnfSAT += "%d 0 " % (var)
cnfSAT = cnfSAT[:-1] + "\n"

#Clausulas de Completitud
for i in range(1, orden**6 + 1, orden**2):
    for j in range(orden**2):
        cnfSAT += "%d " % (i+j)
    cnfSAT += "0\n"

#Clausulas de Unicidad
for i in range(1, orden**6 + 1, orden**2):
    fin = i + orden**2
    for j in range(i, i + orden**2):
        for k in range(j+1, fin):
            cnfSAT += "%d %d 0 " % (-j, -k)
    cnfSAT = cnfSAT[:-1] + "\n"

#Clausulas de Validez
#Por Fila y Columna
for i in range(1, orden**6 + 1, orden**4):
    fin = i + orden**4
    for j in range(i, fin):
        # Fila
        for k in range(j + orden**2, fin, orden**2):
            cnfSAT += "%d %d 0 " % (-j, -k)
        cnfSAT = cnfSAT[:-1] + "\n"
        
        # Columna
        for k in range(j + orden**4, orden**6 +1, orden**4):
            cnfSAT += "%d %d 0 " % (-j, -k)
        cnfSAT = cnfSAT[:-1] + "\n"

#Por Sub Sudoku
def resuelve(a):
    temp = ""
    for i in range(orden**2):
        for j in range(i, len(a), orden**2):
            for k in range(j + orden**2, len(a), orden**2):
                temp += "%d %d 0 " % (-a[j], -a[k])
            temp = temp[:-1] + "\n"
    return(temp)

for i in range(orden):                                      # i = fila de sub-sudokus
    for j in range(orden):                                  # j = columna del sub-sudoku
        a =  []
        for k in range(orden):                              # k = fila dentro del sub-sudoku
            for l in range(orden):                          # l = columna dentro del sub-sudoku
                for m in range(1, orden**2 +1):             # m = variable de la casilla
                    a.append((i * (orden**5)) + (j * (orden**3)) + (k * orden**4) + (l * orden**2) + m)
        cnfSAT += resuelve(a)

print(cnfSAT)