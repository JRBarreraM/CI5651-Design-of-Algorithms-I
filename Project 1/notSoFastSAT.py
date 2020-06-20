file = open("ejemplitoInputSAT.txt", "r")
print(file.readlines())

lines = file.readlines()


numOfClauses = 0
numOfVariables = 0

for line in lines:
    if line[0] == 'c':
        pass
    elif line[0] == 'p':
       line[:-2].split()
       numOfClauses = line[2]
       numOfVariables = line[3]

    else:
        line.split()