import time
import sys
import random
from copy import deepcopy

#funcion limite de tiempo
def timerDone(limit):
    return time.time() - inicio >= limit

#
def simplificar(formula, k):
    i = 0
    while i < len(formula):
        if k in formula[i]:
            del formula[i]
        else:
            try:
                formula[i].remove(-k)
            except:
                pass
            i += 1
    return formula

def actualizarPesos():
    for var in clausulaAnterior:
        contadorVariables[var] += 3

def vsids(clausula):
    pesos = {}
    for var in clausula:
        pesos[var] = contadorVariables[var]
    return max(pesos, key=pesos.get)

def contarOcurrencias(formula):
    apariencias = {}
    for claus in formula:
        for var in claus:
            if var in apariencias:
                apariencias[var] += 1
            else:
                apariencias[var] = 1
    return apariencias


def case1(formulaTemp1):
    while formulaTemp1:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(formulaTemp1[1]):
            #print(formulaTemp1[0])
            actVar = formulaTemp1[0][0]
            if actVar > 0:
                verdad[actVar - 1] = 1
            else:
                verdad[abs(actVar) - 1] = 0

            formulaTemp1 = simplificar(formulaTemp1, actVar)
        else:
            return False

    return True

#
def case2(formulaTemp2, actVar):
    if actVar > 0:
        verdad[actVar - 1] = 1
    else:
        verdad[abs(actVar) - 1] = 0
    
    formulaTemp2 = simplificar(formulaTemp2, actVar)

    if len(formulaTemp2) == 0:
        return True

    while formulaTemp2:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(formulaTemp2[0]) == 0:
            #print("oops")
            actualizarPesos()
            return False
        if len(formulaTemp2[0]) == 1:
            solucion = case1(formulaTemp2)
            if solucion:
                return solucion
        else:
            actualVar = vsids(formulaTemp2[0])
            clausulaAnterior = formulaTemp2[0]
            solucion = case2(deepcopy(formulaTemp2), actualVar)
            clausulaAnterior = formulaTemp2[0]
            if not solucion:
                solucion = case2(deepcopy(formulaTemp2), -(actualVar))
            return solucion

def escribirRespuesta(caso, verdad):
    n = len(verdad)
    if caso == 1:
        print("s cnf 1 %d" % (n))
        for i in range(1, n+1):
            if verdad[i-1] == 1:
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
verdad = []
formula = {}
formula[0] = {}
literales = {}
actualClausula = []
clausulaAnterior = []
contadorVariables = {}

count = 0
#leer el archivo 
for line in lines:
    if line[0] == 'c':
        pass
    elif line[0] == 'p':
        line =  line.split()
        numOfVariables = int(line[2])
        numOfClauses = int(line[3])
        verdad = [None] * numOfVariables

    else:
        line =  line.split()
        numOfLit = len(line)-1
        if numOfLit not in formula:
            formula[numOfLit] = {}
        for elem in line:
            if elem != "0":
                lit = int(elem)
                if lit > 0:
                    if lit not in literales:
                        literales[lit] = [(1, count)]
                    else:
                        literales[lit].append((1, count))
                    if lit not in contadorVariables:
                        contadorVariables[lit] = 1
                    else:
                        contadorVariables[lit] += 1
                else:
                    if -(lit) not in literales:
                        literales[-(lit)] = [(-1,count)]
                    else:
                        literales[-(lit)].append((-1,count))
                    if -(lit) not in contadorVariables:
                        contadorVariables[-(lit)] = 1
                    else:
                        contadorVariables[-(lit)] += 1                    
                actualClausula.append(lit)
            else:
                formula[numOfLit][count] = actualClausula
                count += 1
                actualClausula = []

#si hay o no un 0 al final
numOfLit = len(actualClausula)
if numOfLit != 0 and numOfLit not in formula:
    formula[numOfLit] = {}
    formula[numOfLit][count] = actualClausula

longestClaus = max(formula.keys()

for i in range(1, longestClaus):
    if i not in formula:
        formula[i] = {}

inicio = time.time()
timeLimit = 10

if len(sys.argv) > 2:
    timeLimit = int(sys.argv[2])

# MAIN

if len(formula[1]) > 0:
    solucion = case1(formula)

for i in range(2, longestClaus):
    if formula[i]:
        clausulaEscogida = formula[i][(formula[i].keys())[0]]
        actualVar = vsids(clausulaEscogida)
        clausulaAnterior = clausulaEscogida
        solucion = case2(deepcopy(formula), actualVar)
        clausulaAnterior = clausulaEscogida
        if not solucion:
            solucion = case2(deepcopy(formula), -(actualVar))
        break

if timerDone(timeLimit):
    # No se resolvio
    escribirRespuesta(-1, verdad)

if solucion:
    escribirRespuesta(1, verdad)

escribirRespuesta(0, verdad)