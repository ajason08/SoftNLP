#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

# configuracion inicial: 3 opciones en utf-8 en pycharm/settings/editor, sin el check
# tiene el coding utf-8 en las primeras lineas de este codigo


# CASO 1 el archivo tiene tilde en avilés
#with open('qq.txt', 'r') as f:
 #   myString = f.read().decode('latin-1')       # sin el decode(latin-1) reemplaza 'é' e tildada por '?'
#b= myString.split('\t')
#print b                                         # imprime asi u'Avil\xe9s
#for x in b:
 #  print x                                      # al imprimir cada una la saca bien, avilés


# CASO 2 el texto ingresado tiene caracteres del sgt formato centÃ­metros
with open('ptg.txt', 'r') as f:
    myString = f.read()    # con el decode(latin-1) reemplaza 'í' i tildada por 'Ã­'
b= myString.split('\n')
print b                                          # imprime asi u'Avil\xe9s
i=0
for x in b:
   for xx in x:

       print x, i                                      # al imprimir cada una la saca bien, centímetros
       i=i+1

print b[16]

#muestra el encode de una palabra, y la forma en como luce
#print type(expresion), repr(expresion)