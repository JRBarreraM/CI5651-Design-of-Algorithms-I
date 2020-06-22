#import numpy as np
import time
import sys
import random
from copy import deepcopy

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

#b = a[:]
#b = list(a)
def case1(clausulasTemp1):
    while clausulasTemp1:
        if timerDone(timeLimit):
            # No se resolvio
            print('Time\'s Up')
            break

        if len(clausulasTemp1[0]) == 1:
            #print(clausulasTemp1[0])
            actVar = clausulasTemp1[0][0]
            if actVar > 0:
                variables[actVar - 1] = 1
            else:
                variables[abs(actVar) - 1] = 0

            clausulasTemp1 = simplificar(clausulasTemp1, actVar)
        else:
            return clausulasTemp1

    print("Yeah! in only: %f seconds" % (time.time() - inicio))
    print(variables)
    print(clausulasTemp1)
    sys.exit()

#
def case2(clausulasTemp2, actVar):
    if actVar > 0:
        variables[actVar - 1] = 1
    else:
        variables[abs(actVar) - 1] = 0
    
    #print("Antes de simplify: " + str(len(clausulasTemp2)))
    clausulasTemp2 = simplificar(clausulasTemp2, actVar)
    #print("Despues de simplify: " + str(len(clausulasTemp2)))
    #print(actVar)
    #print()

    if len(clausulasTemp2) == 0:
        print("Yeah! in only: %f seconds" % (time.time() - inicio))
        print(variables)
        print(clausulasTemp2)
        sys.exit()

    while clausulasTemp2:
        if timerDone(timeLimit):
            # No se resolvio
            print('Time\'s Up')
            break

        if len(clausulasTemp2[0]) == 0:
            #print("oops")
            return
        if len(clausulasTemp2[0]) == 1:
            clausulasTemp2 = case1(clausulasTemp2)
        else:
            for k in random.sample(clausulasTemp2[0], len(clausulasTemp[0])):
                case2(deepcopy(clausulasTemp2), k)
            return


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
timeLimit = 90


# MAIN LOOP
while clausulasTemp:
    if timerDone(timeLimit):
        # No se resolvio
        print('Time\'s Up')
        break

    if len(clausulasTemp[0]) == 1:
        clausulasTemp = case1(clausulasTemp)
    else:
        #print(len(clausulasTemp))
        for k in random.sample(clausulasTemp[0], len(clausulasTemp[0])):
            #print(k)
            case2(deepcopy(clausulasTemp), k)
        print("Insatisfacible! in only: %f seconds" % (time.time() - inicio))
        sys.exit()
print("No se pudo resolver en %d" % (timeLimit))