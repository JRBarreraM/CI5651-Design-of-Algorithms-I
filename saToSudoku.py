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
orden = int(numOfVars**(1/6))

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
    resultado += "%d " % (orden)
    for var in finales:
        temp = (var % orden**2)
        if temp == 0:
            temp = orden**2
        resultado += str(temp)
    print(resultado)
#    for i in range(0,len(resultado),9):
#        print(resultado[i:i+9])