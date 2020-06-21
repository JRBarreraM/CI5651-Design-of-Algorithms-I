#import numpy as np
import time
import sys

#funcion limite de tiempo
def timerDone(limit):
    return time.time() - inicio >= limit

#
def simplificar(clausulas, k):
    i = 0
    while i < len(clausulas):
        if k in clausulas[i]:
            #print("Estoy en c: %d" % (k))
            del clausulas[i]
        else:
            #print("No Estoy en c: %d" % (k))
            try:
                clausulas[i].remove(-k)
            except:
                pass
            i += 1
    clausulas.sort(key=len)
    return clausulas

#
def case1(clausulasTemp):
    while clausulasTemp:
        if timerDone(30):
            # No se resolvio
            print('Time\'s Up')
            break

        if len(clausulasTemp[0]) == 1:
            #print(clausulasTemp[0])
            actVar = clausulasTemp[0][0]
            if actVar > 0:
                variables[actVar - 1] = 1
            else:
                variables[abs(actVar) - 1] = 0

            clausulasTemp = simplificar(clausulasTemp, actVar)
        else:
            return clausulasTemp

    print("Yeah! in only: %f seconds" % (time.time() - inicio))
    print(variables)
    print(clausulasTemp)
    sys.exit()

#
def case2(clausulasTemp, variables, actVar):

    if actVar > 0:
        variables[actVar - 1] = 1
    else:
        variables[abs(actVar) - 1] = 0

    clausulasTemp = simplificar(clausulasTemp, actVar)

    while clausulasTemp:
        if timerDone(30):
            # No se resolvio
            print('Time\'s Up')
            break

        if len(clausulasTemp[0]) == 1:
            clausulasTemp = case1(clausulasTemp)
        else:
            for k in clausulasTemp[0]:
                case2(clausulasTemp, variables, k)
            return False

############################################################
#file = open("parabarrera.txt", "r")
file = open("ejemplitoInputSAT.txt", "r")
#file = open("satEntry.txt", "r")
lines = file.readlines()

numOfClauses = 0
numOfVariables = 0
variables = []
#variables = np.zeros(0)
clausulas = []
actualClausula = []

#leer el archivo 
for line in lines:
    if line[0] == 'c':
        pass
    elif line[0] == 'p':
        line =  line.split()
        numOfVariables = int(line[2])
        numOfClauses = int(line[3])
        variables = [None] * numOfVariables
        #variables = np.zeros(numOfVariables)
        #variables[:] = np.NaN

    else:
        line =  line.split()
        for elem in line:
            if elem != "0":
                actualClausula.append(int(elem))
            else:
                clausulas.append(actualClausula)
                actualClausula = []

#si hay o no un 0 al final
if len(actualClausula) != 0:
    clausulas.append(actualClausula)

inicio = time.time()
clausulasTemp = clausulas
clausulasTemp.sort(key=len)

while clausulasTemp:
    if timerDone(10):
        # No se resolvio
        print('Time\'s Up')
        break

    if len(clausulasTemp[0]) == 1:
        clausulasTemp = case1(clausulasTemp)
    else:
        for k in clausulasTemp[0]:
            case2(clausulasTemp, variables, k)

print("No se pudo resolver")