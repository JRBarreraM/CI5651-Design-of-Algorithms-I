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
            del clausulas[i]
        else:
            try:
                clausulas[i].remove(-k)
            except:
                pass
            i += 1
    clausulas.sort(key=len)
    return clausulas

def actualizarPesos():
    for var in clausulaAnterior:
        contadorVariables[var] += 3

def vsids(clausula):
    pesos = {}
    for var in clausula:
        if var in pesos:
            pesos[var] = contadorVariables[var]
    return max(pesos, key=pesos.get)

def contarOcurrencias(clausulas):
    apariencias = {}
    for claus in clausulas:
        for var in claus:
            if var in apariencias:
                apariencias[var] += 1
            else:
                apariencias[var] = 1
    return apariencias

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
    
    clausulasTemp2 = simplificar(clausulasTemp2, actVar)

    if len(clausulasTemp2) == 0:
        return True

    while clausulasTemp2:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(clausulasTemp2[0]) == 0:
            #print("oops")
            actualizarPesos()
            return False
        if len(clausulasTemp2[0]) == 1:
            solucion = case1(clausulasTemp2)
            if solucion:
                return solucion
        else:
            actualVar = vsids(clausulasTemp2[0])
            clausulaAnterior = clausulasTemp2[0]
            solucion = case2(deepcopy(clausulasTemp2), actualVar)
            clausulaAnterior = clausulasTemp2[0]
            if not solucion:
                solucion = case2(deepcopy(clausulasTemp2), -(actualVar))
            return solucion

def escribirRespuesta(caso, variables):
    n = len(variables) +1
    if caso == 1:
        print("s cnf 1 %d" % (n))
        for i in range(1, n):
            if variables[i-1] == 1:
                print("v %d" % (i))
            else:
                print("v %d" % (-(i)))

    elif caso == 0:
        print("s cnf 0 %d" % (n))
        
    elif caso == -1:
        print("s cnf -1 %d" % (n))
    sys.exit()

############################################################
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

numOfClauses = 0
numOfVariables = 0
variables = []
clausulas = []
actualClausula = []
contadorVariables = contarOcurrencias(clausulas)
clausulaAnterior = []

#leer el archivo 
for line in lines:
    if line[0] == 'c':
        pass
    elif line[0] == 'p':
        line =  line.split()
        numOfVariables = int(line[2])
        numOfClauses = int(line[3])
        variables = [None] * numOfVariables

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
clausulas.sort(key=len)
timeLimit = 10

# MAIN

if len(clausulas[0]) == 1:
    solucion = case1(clausulas)
    
if len(clausulas) >= 1:
    actualVar = vsids(clausulas[0])
    clausulaAnterior = clausulas[0]
    solucion = case2(deepcopy(clausulas), actualVar)
    clausulaAnterior = clausulas[0]
    if not solucion:
        solucion = case2(deepcopy(clausulas), -(actualVar))

if timerDone(timeLimit):
    # No se resolvio
    escribirRespuesta(-1, variables)

if solucion:
    escribirRespuesta(1, variables)

escribirRespuesta(0, variables)