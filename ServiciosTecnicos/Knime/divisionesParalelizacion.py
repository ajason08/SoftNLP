inicio = 1000
final = 5000
factorDivision = 4
cociente = (final-inicio+1)/factorDivision-1
print cociente
sectorIn = []
sectorFin = []
ultimo=inicio
for i in range(1,factorDivision):
    sectorIn.append(ultimo)
    ultimo = ultimo+cociente
    sectorFin.append(ultimo)
    ultimo = ultimo+1
sectorIn.append(ultimo)
sectorFin.append(final)

for i in range(len(sectorIn)):
    print sectorIn[i], sectorFin[i]