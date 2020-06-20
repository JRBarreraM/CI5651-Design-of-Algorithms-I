#import numpy as np

file = open("ejemplitoInputSAT.txt", "r")
lines = file.readlines()

numOfClauses = 0
numOfVariables = 0
variables = []
clausulas = []
actualClausula = []
for line in lines:
    if line[0] == 'c':
        pass
    elif line[0] == 'p':
        line =  line.split()
        numOfClauses = int(line[2])
        numOfVariables = int(line[3])
        variables = [0] * numOfVariables
    else:
        line =  line.split()
        for elem in line:
            if elem != "0":
                actualClausula.append(elem)
            else:
                clausulas.append(actualClausula)
                actualClausula = []

if len(actualClausula) != 0:
    clausulas.append(actualClausula)

print(clausulas)
print(variables)
