#import numpy as np
import time

inicio = time.time()
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

def validClausula(clausula):
    for k in clausula:
        if k > 0 and variables[k-1] == 1:
            return True
        elif k < 0 and variables[(-k)-1] == 0:
            return True
    return False

#funcion limite de tiempo
def timerDone(limit):
    return time.time() - inicio >= limit


def fijarConstantes(actClausula):
    while len(clausulas[actClausula]) == 1:
        if abs(clausulas[actClausula][0]) not in constantes:
            if clausulas[actClausula][0] > 0:
                variables[(clausulas[actClausula][0]) - 1] = 1
                constantes.append(clausulas[actClausula][0])
            else:
                variables[(clausulas[actClausula][0]) - 1] = 0
                constantes.append(abs(clausulas[actClausula][0]))
        else:
            if not ((clausulas[actClausula][0] > 0 and variables[(clausulas[actClausula][0]) -1] == 1)
                or (clausulas[actClausula][0] < 0 and variables[ abs(clausulas[actClausula][0]) - 1] == 0)):
                #insatisfacible
                print('insatisfacible')
                pass
        actClausula += 1
    return actClausula


def notInFijados(var):
    for par in fijados:
        if par[0] == var:
            return False
    return True


def checkFail(variables):
    for clausCombination in fails:
        foundError = True
        for varCombination in clausCombination:
            if variables[varCombination[0] - 1] != varCombination[1]:
                foundError = False
                break
        if foundError:
            return True
    return False


clausulas.sort(key=len)
actClausula = 0
constantes = []
fijados = [] #[[var,clause]]
actVariable = 0
error = False
fails = []
#########################################################################

actClausula = fijarConstantes(actClausula)

while actClausula != numOfClauses:
    #print('actClaus: ' + str(actClausula))
    #print('actVar: ' + str(actVariable))
    #print('Fijados: ' + str(fijados))
    #print('fail: '+ str(fails))
    #print('Var: ' + str(variables))
    #print()


    if timerDone(300):
        # No se resolvio
        print('Time\'s Up')
        break

    if validClausula(clausulas[actClausula]):
        actClausula += 1
        actVariable = 0
    else:
        if actVariable >= len(clausulas[actClausula]):
            if actClausula == len(constantes):
                print("insatisfacible")
                break
            failureCombination = []
            detectNone = False
            for k in clausulas[actClausula]:
                var = abs(k)
                #if variables[var-1] == np.NaN:
                if variables[var-1] == None:
                    detectNone = True
                    break
                failureCombination.append([var,variables[var-1]]) #[[var,val]]
            if not detectNone:
                fails.append(failureCombination)

            ultFijado = fijados.pop()
            actClausula = ultFijado[1]
            try:
                actVariable = clausulas[actClausula].index(ultFijado[0])
            except:
                actVariable = clausulas[actClausula].index(-ultFijado[0])
            #variables[ultFijado[0] - 1] = np.NaN
            variables[ultFijado[0] - 1] = None
            actVariable += 1

        elif (abs(clausulas[actClausula][actVariable]) not in constantes) and (notInFijados(abs(clausulas[actClausula][actVariable]))):
                if clausulas[actClausula][actVariable] > 0:
                    variables[clausulas[actClausula][actVariable] - 1] = 1
                else:
                    variables[abs(clausulas[actClausula][actVariable]) - 1] = 0

                if checkFail(variables):
                    #variables[abs(clausulas[actClausula][actVariable]) - 1] = np.NaN
                    variables[abs(clausulas[actClausula][actVariable]) - 1] = None
                    actVariable += 1
                    #print('fail detected')
                else:
                    k = abs(clausulas[actClausula][actVariable])                    
                    fijados.append([k,actClausula])
        else:
            actVariable += 1

print("Yeah! in only: %f seconds" % (time.time() - inicio))
print(variables)