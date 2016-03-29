#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import re
import xlrd
import xlwt
from pandas import *
import prettytable
from operator import itemgetter


def cargarArchivoTaggerTNT(archivo):
    palabras = []
    categorias = []
    lemas = []
    with open(archivo, 'r') as f:
        myString = f.read()    # con el decode(latin-1) reemplaza 'í' i tildada por 'Ã­'
    b= myString.split('\n')
    i=0

    if b[-1].split('\t')==['']: # se elimina si al final no saco la ultima linea completa
        b=b[0:-1]

    for x in b:
        t=1
        bb= x.split('\t')
        if len(bb)<>3:
            print "aqui esta", bb
        for xx in bb:
         #   print "celda", xx, i
            if i%3==0:
                palabras.append(xx)
            elif i%3==1:
                categorias.append(xx)
            elif i%3==2:
                lemas.append(xx)                                     # al imprimir cada una la saca bien, centímetros
            i=i+1

    return palabras, categorias, lemas




def cargarcsv(archivo, signoSeparacion=","):
    with codecs.open(archivo,'r',encoding='iso-8859-1') as f:
        myString = f.read()    # con el decode(latin-1) reemplaza 'í' i tildada por 'Ã­'
    b= myString.split(signoSeparacion)
    return  b

def exportarExcelClasificacion(urls, clasificacion, nombre="outputClasificacion.xls"):
    style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet',cell_overwrite_ok=True)
    ws.write(0, 0, 'LINK', style0)
    ws.write(0, 1, 'CLASIFICACION', style0)
    for i in range (len(urls)):
        #ws.write(i+1, 0, articulos[i])
        ws.write(i+1, 0, urls[i])
        ws.write(i+1, 1, clasificacion[i])
    wb.save(nombre)
    print "Archivo exportado como", nombre

def exportarExcel(dataframe, nombreArchivoExcel="outputDataframe.xls"):

    style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')

    nombres = list(dataframe.columns.values)
    wb = xlwt.Workbook(encoding='latin-1')
    ws = wb.add_sheet('my Sheet',cell_overwrite_ok=True)
    for i in range (len(nombres)):
        nom = nombres[i]
        ws.write(0, i, nom, style0)
    #nose si no muestra el ultimo
    for filai in range (1,len(dataframe.axes[0])):
        for columnaj in range (len(nombres)):
            col = nombres[columnaj]
            a = (dataframe.get_value(dataframe.index[filai],col))
            if len(a)>30000:
                a = "muy largo"
            ws.write(filai, columnaj,a)
        wb.save(nombreArchivoExcel)
    print "Archivo exportado como", nombreArchivoExcel

def exportarMatrizCSV(dataframe, nombreArchivo="outputDataframe.csv", separadorCol = "$$", separadorFilas = "\n"):
    nombres = list(dataframe.columns.values)
    quo = "<quote>"
    outputArt=open(nombreArchivo,"w")
    outputArt.close()   # Reinicio txt
    outputArt = open(nombreArchivo,"a")
    #guardo cabecera de la tabla
    for nomColi in range (len(nombres)):
        nom = quo+nombres[nomColi]+quo+separadorCol
        outputArt.write(nom)
    outputArt.write(separadorFilas)
    for filai in range (0,len(dataframe.axes[0])):
        for nomColi in range (len(nombres)):
            nom = nombres[nomColi]
            valorCelda = quo+dataframe.get_value(dataframe.index[filai],nom)+quo+separadorCol
            outputArt.write(valorCelda)
        outputArt.write(separadorFilas)
    outputArt.close()
def cargarLematizacion2(archivo):
    tagger = []
    with open(archivo, 'r') as f:
        myString = f.read()    # con el decode(latin-1) reemplaza 'í' i tildada por 'Ã­'
    b= myString.split('\n')
    i=0
    for x in b:
        bb= x.split('\t')
        tagger.append(bb)
    return tagger

def ordenarTabla(columnas,c):
    #ordena una matriz procedente de vectores de la forma [vector0, vector1, vectorn],
    #c es el numero del vector por el cual se ordenara la matriz
    if not c in range(len(columnas)):
        print "Excepcion c is not in range of matrix"
        return None
    nroFilas=len(columnas[0])
    matriz = []
    for i in range(nroFilas):
        fila= []
        for columna in columnas:
            fila.append(columna[i])
        matriz.append(fila)
    x = sorted(matriz, key=itemgetter(c))
    return x

def cargarColumnaEnLista(excel, hoja, columna, filainicial=0, filaLimite=0):
    # dado un archivo excel, una hoja y una columna(inicia en 0) se cargaran los datos en una
    # hasta llegar a una celda vacia o hasta la fila limite establecida
    doc = xlrd.open_workbook(excel)
    sheet = doc.sheet_by_index(hoja)
    if filaLimite == 0:
        nrows = sheet.nrows
        filaLimite = nrows
    lista = []
    for i in range(filainicial, filaLimite):
        #print filaLimite
        try:
            celda = sheet.cell_value(i,columna).__str__()
            if celda == '':                                   # una celda vacia indica que la columna no tiene mas valores
                break
            lista.append(celda.encode())
        except:
            celda= sheet.cell_value(i, columna)
            #print celda, "execepcion!!", sys.exc_info()[0]
            #continue
            if celda=='':                                   # una celda vacia indica que la columna no tiene mas valores
                break
            lista.append(celda.encode('utf-8'))# el encode lo agregue para que no saque las palabras tildadas como unicode
    return lista

def is_ascii(s):
    try:
        return all(ord(c) < 128 for c in s)
    except TypeError:
        return False