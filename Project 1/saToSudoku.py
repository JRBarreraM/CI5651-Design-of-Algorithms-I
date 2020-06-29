import sys

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

line =  lines[0].split()
case = int(line[2])
numOfVars = int(line[3])

finales = []

resultado = ""

if case == 0:
    print("Insatisfacible")
elif case == -1:
    print("No se pudo resolver")
else:
    for i in range(1, numOfVars+1):
        if int(lines[i].split()[1]) > 0:
            finales.append(i)
    resultado += "%d " % (int(len(finales)**0.25))
    for var in finales:
        resultado += str((var % 9))
    print(resultado)
#    for i in range(0,len(resultado),9):
#        print(resultado[i:i+9])