import time
import sys
import os

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

for i in range(len(lines)):
    if len(lines[i]) < 3:
        lines.pop(i)

os.system("touch sudoku.txt")
os.system("touch sat.txt")
os.system("touch satSolucion.txt")
os.system("touch soluciones.txt")
os.system("truncate -s 0 soluciones.txt")

tiemposSlow = []
tiemposZchaff = []

#print(lines)
for sudoku in lines:

#sudoku = lines[9]

    #os.system("echo %s >> sudoku.txt" % (sudoku))
    data=open("sudoku.txt", "w")
    data.write(sudoku)
    data.close()
    os.system("python3 sudokuToSad.py sudoku.txt >> sat.txt")

    inicio = time.time()
    os.system("python3 slowSAT.py sat.txt >> satSolucion.txt")
    tiempoSlow = time.time() - inicio
    tiemposSlow.append(tiempoSlow)

    inicio = time.time()
    os.system("zchaff64/zchaff sat.txt 10 >> /dev/null")
    #print(sudoku)
    tiempoZchaff = time.time() - inicio
    tiemposZchaff.append(tiempoZchaff)

    os.system("python3 saToSudoku.py satSolucion.txt >> soluciones.txt")

    os.system("truncate -s 0 sudoku.txt sat.txt satSolucion.txt")

os.system("rm sudoku.txt sat.txt satSolucion.txt")

print("Tiempo slowSat | Tiempo Zchaff")
for i in range(len(tiemposSlow)):
    print("%f | %f"  % (tiemposSlow[i], tiemposZchaff[i]))

import matplotlib.pyplot as plt

p1 = plt.plot(tiemposSlow)
p2 = plt.plot(tiemposZchaff)
plt.ylabel('Segundos')
plt.xlabel('Instancia Sudoku')
plt.title('slowSAT vs Zchaff')
plt.suptitle('Tiempo Maximo Aceptable 10 segundos')
plt.legend((p1[0], p2[0]), ('slowSAT', 'Zchaff'))
plt.grid(True)
plt.show()