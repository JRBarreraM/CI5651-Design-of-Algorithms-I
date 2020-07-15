import time
import sys
import random
from copy import deepcopy

#funcion limite de tiempo
def timerDone(limit):
    return time.time() - inicio >= limit

def tamOfClausula(formula, key, clausulasSatisfechas):
    for i in range(longestClaus+1):
        tam = formula[i].get((key))
        if tam != None:
            return i
    for i in clausulasSatisfechas:
        if i[0] == key:
            return i[1]
    return None
#
def simplificar(formula, k, clausulasSatisfechas):
    clausulasConK = literales[abs(k)]
    for claus in clausulasConK:
        tam = tamOfClausula(formula, claus[0], clausulasSatisfechas)
        clausula = formula[tam].pop(claus[0], None)
        if clausula != None:
            #print(" claus: " + str(clausula))
            if k * claus[1] > 0:
                clausulasSatisfechas.append([claus[0], tam, clausula])
            else:
                #tamOfClaus[claus[0]] -= 1
                formula[tam -1][claus[0]] = clausula
            #print("tam: " + str(tam) + " -> " + str(tamOfClausula(formula, claus[0], clausulasSatisfechas)))
    #print(formula)
    return formula

def actualizarPesos():
    for var in clausulaAnterior:
        contadorVariables[var] += 3

def vsids(clausula):
    pesos = {}
    for var in clausula:
        pesos[var] = contadorVariables[var]
    return max(pesos, key=pesos.get)


def case1(formulaTemp1, verdadTemp, clausulasSatisfechas):
    while len(clausulasSatisfechas) != numOfClauses:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(formulaTemp1[1]):
            temp = list(formulaTemp1[1].values())
            for var in temp[0]:
                #print(temp[0])
                if verdadTemp[abs(var)-1] == None:
                    if var > 0:
                        verdadTemp[var - 1] = 1
                    else:
                        verdadTemp[abs(var) - 1] = 0
                    formulaTemp1 = simplificar(formulaTemp1, var, clausulasSatisfechas)
                    break
        else:
            return False

    global verdad
    verdad = verdadTemp
    #print(verdadTemp)
    return True

#
def case2(formulaTemp2, verdadTemp, clausulasSatisfechas, actVar):
    if actVar > 0:
        verdadTemp[actVar - 1] = 1
    else:
        verdadTemp[abs(actVar) - 1] = 0
    
    formulaTemp2 = simplificar(formulaTemp2, actVar, clausulasSatisfechas)
    if len(clausulasSatisfechas) == numOfClauses:
        #print(clausulasSatisfechas)
        global verdad 
        verdad = verdadTemp
        return True

    while len(clausulasSatisfechas) != numOfClauses:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(formulaTemp2[0]) != 0:
            #print("oops")
            actualizarPesos()
            return False
        if len(formulaTemp2[1]) != 0:
            #print("Caso 2 llama a caso 1")
            solucion = case1(formulaTemp2, verdadTemp, clausulasSatisfechas)
            if solucion:
                return solucion
        else:
            for i in range(2, longestClaus +1):
                if formulaTemp2[i]:
                    clausulaEscogida = formulaTemp2[i][list(formulaTemp2[i].keys())[0]]
                    actualVar = vsids(clausulaEscogida)
                    clausulaAnterior = clausulaEscogida
                    solucion = case2(deepcopy(formulaTemp2), deepcopy(verdadTemp), deepcopy(clausulasSatisfechas), actualVar)
                    clausulaAnterior = clausulaEscogida
                    if not solucion:
                        solucion = case2(deepcopy(formulaTemp2), deepcopy(verdadTemp), deepcopy(clausulasSatisfechas),-(actualVar))
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
clausulasSatisfechas = []
tamOfClaus = {}
count = 0
numOfLit = 0

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
        for elem in line:
            if elem != "0":
                lit = int(elem)
                if lit > 0:
                    if lit not in literales:
                        literales[lit] = [(count,1)]
                    else:
                        literales[lit].append((count, 1))
                else:
                    if -(lit) not in literales:
                        literales[-(lit)] = [(count, -1)]
                    else:
                        literales[-(lit)].append((count, -1))
                
                if lit not in contadorVariables:
                    contadorVariables[lit] = 1
                else:
                    contadorVariables[lit] += 1
                actualClausula.append(lit)
            else:
                numOfLit = len(actualClausula)
                if numOfLit not in formula:
                    formula[numOfLit] = {}
                formula[numOfLit][count] = actualClausula
                tamOfClaus[count] = numOfLit
                count += 1
                actualClausula = []

#si hay o no un 0 al final
numOfLit = len(actualClausula)
if numOfLit != 0 and numOfLit not in formula:
    formula[numOfLit] = {}
    formula[numOfLit][count] = actualClausula
    tamOfClaus[count] = numOfLit

longestClaus = max(formula.keys())

for i in range(1, longestClaus +1):
    if i not in formula:
        formula[i] = {}

inicio = time.time()
timeLimit = 10

if len(sys.argv) > 2:
    timeLimit = int(sys.argv[2])

# MAIN

if len(formula[1]) > 0:
    solucion = case1(formula, verdad, clausulasSatisfechas)

for i in range(2, longestClaus + 1):
    if formula[i]:
        clausulaEscogida = formula[i][list(formula[i].keys())[0]]
        actualVar = vsids(clausulaEscogida)
        clausulaAnterior = clausulaEscogida
        solucion = case2(deepcopy(formula), deepcopy(verdad), deepcopy(clausulasSatisfechas), actualVar)
        clausulaAnterior = clausulaEscogida
        if not solucion:
            solucion = case2(deepcopy(formula), deepcopy(verdad), deepcopy(clausulasSatisfechas), -(actualVar))
        break

if timerDone(timeLimit):
    # No se resolvio
    escribirRespuesta(-1, verdad)
    
if solucion:
    escribirRespuesta(1, verdad)

escribirRespuesta(0, verdad)