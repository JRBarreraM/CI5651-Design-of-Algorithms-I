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

def encontrarLiteral(clasulas):
    for k in clasulas:
        if len(k) == 1:
            return True
    return False

def masComun(clausulas):
    apariencias = {}
    for claus in clausulas:
        for var in claus:
            if var in apariencias:
                apariencias[var] += 1
            else:
                apariencias[var] = 1
    return max(apariencias, key=apariencias.get)

def seleccionAleatoria(clausulas):
    return random.choice(random.choice(clausulas))

def case1(clausulasTemp1):
    while clausulasTemp1:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(clausulasTemp1[0]) == 1:
            #print(clausulasTemp1[0])
            actVar = clausulasTemp1[0][0]
            if actVar > 0:
                variables[actVar - 1] = 1
            else:
                variables[abs(actVar) - 1] = 0

            clausulasTemp1 = simplificar(clausulasTemp1, actVar)
        else:
            return False

    return True

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
        return True

    while clausulasTemp2:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(clausulasTemp2[0]) == 0:
            #print("oops")
            return False
        if len(clausulasTemp2[0]) == 1:
            solucion = case1(clausulasTemp2)
            if solucion:
                return solucion
        else:
            #solucion = case2(deepcopy(clausulasTemp2), seleccionAleatoria(clausulasTemp2))
            solucion = case2(deepcopy(clausulasTemp2), masComun(clausulasTemp2))
            if not solucion:
                #solucion = case2(deepcopy(clausulasTemp2), -(seleccionAleatoria(clausulasTemp2)))
                solucion = case2(deepcopy(clausulasTemp2), -(masComun(clausulasTemp2)))
            return solucion
    


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
timeLimit = 50

# MAIN

if len(clausulasTemp[0]) == 1:
    solucion = case1(clausulasTemp)
    
if len(clausulasTemp) >= 1:
    solucion = case2(deepcopy(clausulasTemp), seleccionAleatoria(clausulasTemp))
    if not solucion:
        solucion = case2(deepcopy(clausulasTemp), -(seleccionAleatoria(clausulasTemp)))

if timerDone(timeLimit):
    # No se resolvio
    print("No se pudo resolver en %d" % (timeLimit))
    sys.exit()

if solucion:
    print("Yeah! in only: %f seconds" % (time.time() - inicio))
    print(variables)
    #print(clausulasTemp)
    sys.exit()

print("Insatisfacible! in only: %f seconds" % (time.time() - inicio))
sys.exit()