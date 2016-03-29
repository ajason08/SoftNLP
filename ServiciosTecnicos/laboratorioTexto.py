#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlwt
import string
from AnalisisLinguistico.AnalisisMorfologico import *


#from operator import itemgetter, attrgetter

def ordenarTablaFrecuencias(palabras, cantidad, valor, columna):
    matriz = []
    for i in range(len(palabras)):
        fila= []
        fila.append(palabras[i])
        fila.append(cantidad[i])
        fila.append(valor[i])
        matriz.append(fila)
    x = sorted(matriz, key=itemgetter(columna))
    return x

print u'\xe1'

a = 'itemprop="name">Eln acoge propuesta para iniciar dlogo de paz con el Gobierno</h1>                             <h2 itemprop="description">La propuesta fue hecha por el colectivo Colombianos y Colombianas por la Paz (CCP).</h2>                         </hgroup> '
print getOcurrenciasExpresion(a,"<h2", "</h2>")



exit()
print 1*1.0/3

palabra = "murio"
a = "Pedro Luis  murio"
if a.__contains__(palabra):
    print "la contiene"
else:
    print "no contiene"


conectoresNombres = "de,del,los,la,las,y".split(",")
print conectoresNombres

if conectoresNombres.__contains__("la"):
    print "si esta"
else:
    print "no esta"


exit()




style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet',cell_overwrite_ok=True)
ws.write(0, 0, 'Test', style0)
ws.write(2, 0, 4)
ws.write(2, 1, 1)
ws.write(2, 2, xlwt.Formula("A3+B3"))
wb.save('example.xls')


exit()
x= "so i did not for be bad man, i just defend my rights"
patronFin = "just"
indicein = x.find("be")
indiceFin= x.find(patronFin,indicein)
print x[indicein:indiceFin]

hola = [[],[]]

hola[0].append(4)
hola[1].append(5)
print hola[1][0]