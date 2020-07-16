import time
import sys
import random
from copy import deepcopy

#funcion limite de tiempo
def timerDone(limit):
    return time.time() - inicio >= limit
#
def simplificar(k):
    
    reducidas = []
    satisfechas = []
    evento = [abs(k)]
    clausulasConK = literales[abs(k)]
    for claus in clausulasConK:
        tam = tamOfClausula[claus[0]]
        clausula = formula[tam].pop(claus[0], None)
        if clausula != None:
            if k * claus[1] > 0:
                clausulasSatisfechas[claus[0]] = (tam, clausula)
                satisfechas.append(claus[0])
            else:
                formula[tam -1][claus[0]] = clausula
                tamOfClausula[claus[0]] -= 1
                reducidas.append(claus[0])
    evento.append(reducidas)
    evento.append(satisfechas)
    pilaDeEventos.append(evento)

def complicar(k):
    evento = [k+1]
    while evento[0] != abs(k):
        evento = pilaDeEventos.pop()
        verdad[evento[0] -1] = None
        for redu in evento[1]:
            tam = tamOfClausula[redu]
            clausula = formula[tam].pop(redu)
            formula[tam +1][redu] = clausula
            tamOfClausula[redu] += 1
        for satis in evento[2]:
            claus = clausulasSatisfechas.pop(satis)
            formula[claus[0]][satis] = claus[1]

def actualizarPesos():
    for claus in list(formula[0].values()):
        for var in claus:
            #if verdad[abs(var) - 1] == None:
            contadorVariables[var] += 3

def vsids(clausula):
    pesos = {}
    for var in clausula:
        if verdad[abs(var) - 1] == None:
            pesos[var] = contadorVariables[var]
    return max(pesos, key=pesos.get)


def case1():
    global formula
    global contador1
    contador1 += 1
    while len(clausulasSatisfechas) != numOfClauses:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(formula[1]):
            temp = list(formula[1].values())
            for var in temp[0]:
                if verdad[abs(var)-1] == None:
                    if var > 0:
                        verdad[var - 1] = 1
                    else:
                        verdad[abs(var) - 1] = 0
                    simplificar(var)
                    break
        else:
            return False
    return True

#
def case2(actVar):
    global contador2
    contador2 += 1
    if actVar > 0:
        verdad[actVar - 1] = 1
    else:
        verdad[abs(actVar) - 1] = 0
    
    simplificar(actVar)
    if len(clausulasSatisfechas) == numOfClauses:
        return True

    while len(clausulasSatisfechas) != numOfClauses:
        if timerDone(timeLimit):
            # No se resolvio
            return False

        if len(formula[0]) != 0:
            #print("oops")
            actualizarPesos()
            return False
        if len(formula[1]) != 0:
            solucion = case1()
            if solucion:
                return solucion
        else:
            '''
            for i in range(2, longestClaus +1):
                if formula[i]:
                    clausulaEscogida = formula[i][list(formula[i].keys())[0]]
                    #actualVar = vsids(clausulaEscogida)
            '''
            for k in sorted(contadorVariables, key=contadorVariables.get):
                if verdad[abs(k)-1] == None:
                    actualVar = k
                    break
            #clausulaAnterior = clausulaEscogida
            solucion = case2(actualVar)
            #clausulaAnterior = clausulaEscogida
            if not solucion:
                complicar(actualVar)
                solucion = case2(-(actualVar))
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
clausulasSatisfechas = {}
tamOfClausula = {}
pilaDeEventos = []
count = 0
numOfLit = 0

contador1 = 0
contador2 = 0

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
                tamOfClausula[count] = numOfLit
                count += 1
                actualClausula = []

#si hay o no un 0 al final
numOfLit = len(actualClausula)
if numOfLit != 0 and numOfLit not in formula:
    formula[numOfLit] = {}
    formula[numOfLit][count] = actualClausula
    tamOfClausula[count] = numOfLit

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
    solucion = case1()

for i in range(2, longestClaus + 1):
    if formula[i]:
        clausulaEscogida = formula[i][list(formula[i].keys())[0]]
        actualVar = vsids(clausulaEscogida)
        clausulaAnterior = clausulaEscogida
        solucion = case2(actualVar)
        clausulaAnterior = clausulaEscogida
        if not solucion:
            complicar(actualVar)
            solucion = case2(-(actualVar))
        break

#print(contador1)
#print(contador2)

if timerDone(timeLimit):
    # No se resolvio
    escribirRespuesta(-1, verdad)
    
if solucion:
    escribirRespuesta(1, verdad)

escribirRespuesta(0, verdad)