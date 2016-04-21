#!/usr/bin/python
# -*- coding: utf-8 -*-
from GestorEntradasSalidas import *

'''
Ejemplo de basic json
HAIR: Black	#$#HEIGHT: Tall	#$#NATIONALITY (or IDENTITY NUMBER): Afghan#$#DISTINGUISHING CHARACTERISTICS: Shrapnel wound to the right eye
'''

# Este es el nombre de la columna knime en la que cada fila representa un json
nameJsonRow ="caracteristicas"
separador = "#$#"

# todas las claves existentes deben listarse aqui, de lo contrario dara un fallo "mal" por cada vez
claves=[]
claves.append('ALIASESNAME_VARIANTS')
claves.append('BUILD')
claves.append('CITIZENSHIP')
claves.append('CLAN')
claves.append('COMPLEXION')
claves.append('DATE_BIRTH')
claves.append('DATES_USED')
claves.append('CHARACTERISTICS')
claves.append('EYES')
claves.append('HAIR')
claves.append('HEIGHT')
claves.append('LANGUAGES')
claves.append('LOCATION')
claves.append('NATIONALITY')
claves.append('OCCUPATION')
claves.append('PASSPORT')
claves.append('PLACE_OF_BIRTH')
claves.append('RACE')
claves.append('REMARKS')
claves.append('STATUS')
claves.append('WEIGHT')

claves.append('fallo')

nameFile= "myfile.txt"
file = open(nameFile, 'w+')

#creo variables
for clave in claves:
    file.write(clave+"=[]\n")

# creo primera parte primer ciclo
file.write("for json in input_table['"+nameJsonRow+"']:\n")
for clave in claves:
    file.write("\t"+clave+'_var = "none"\n')
file.write("\tfueNone = False\n")

# creo primera parte segundo ciclo (el if none)
file.write('\tfor claveValor in json.split("'+separador+'"):\n')
file.write('\t\tif claveValor =="none":\n')
for clave in claves:
    file.write("\t\t\t"+clave+'.append(claveValor)\n')
file.write('\t\t\tfueNone = True\n')
file.write('\t\t\tbreak\n')

# creo segunda parte segundo ciclo (el if not none)
file.write('\t\tinit = claveValor.index(":")\n')
file.write('\t\tclave = claveValor[:init].strip()\n')
file.write('\t\tvalor = claveValor[init+1:].strip()\n')
for i in range(len(claves)):
    if i==0:
        file.write("\t\tif clave == '"+claves[i]+"':\n")
        file.write("\t\t\t"+claves[i]+"_var= valor\n")
    elif i ==len(claves)-1:
        file.write("\t\telse:\n")
        file.write("\t\t\tfallo_var = 'mal'\n")
    else:
        file.write("\t\telif clave == '"+claves[i]+"':\n")
        file.write("\t\t\t"+claves[i]+"_var= valor\n")

# creo segunda parte primer ciclo (los append)
file.write('\tif fueNone:\n')
file.write('\t\tcontinue\n')
for clave in claves:
    file.write('\t'+clave+'.append('+clave+"_var"+')\n')

# creo tablas de output de knime
file.write('output_table = DataFrame({\n')
for i in range(len(claves)-1):
    file.write("'"+claves[i]+"':"+claves[i]+",\n")
file.write("'"+claves[-1]+"':"+claves[-1]+"\n")
file.write('})\n')


#Muestro Script creado
file = open(nameFile, 'r')
print file.read()

