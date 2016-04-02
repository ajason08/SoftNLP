#!/usr/bin/python
# -*- coding: utf-8 -*-
import GestorEntradasSalidas
from pandas import *
import unicodedata



def indiceVector(vector, word):
    try:
        pos = vector.index(word)
    except ValueError:
        pos=-1 
    return pos

def remove_accents(data):
    newData = []
    for palabra in data.split():
        newData.append(''.join(x for x in unicodedata.normalize('NFKD', palabra) if unicodedata.category(x)[0] == 'L').lower())
    return " ".join(newData)
def limpiarTexto(texto, diccionario):
    for palabraSucia in diccionario:
        try:
            if texto.__contains__(palabraSucia):
                texto = texto.replace(palabraSucia, "")
        except:
            palabraSucia = palabraSucia.decode("utf-8")
            if texto.__contains__(palabraSucia):
                texto = texto.replace(palabraSucia, "")
    return texto

def getSimilitudMorfologicaEn2CorpusTextuales(textosA, textosB, umbral=0.5):
    puntuacion = [".", ",", ":", ";" "?", "¿", "!", "¡", '"',"'", "#"]
    nuevosTextosA = []
    nuevosTextosB = []
    relacionAB = []

    textosASinPuntuacion = []
    textosBSinPuntuacion = []

    for textoA in textosA:
        textoLimpio = remove_accents(limpiarTexto(textoA,puntuacion))
        textosASinPuntuacion.append(textoLimpio)

    for textoB in textosB:
        textoLimpio = remove_accents(limpiarTexto(textoB,puntuacion))
        textosBSinPuntuacion.append(textoLimpio)

    contadorA = 0
    for textoA in textosASinPuntuacion:
        textoAPal = textoA.split()
        contadorB =0
        for textoB in textosBSinPuntuacion:
            textoBPal = textoB.split()
            contador = 0
            ''' pendiente para prueba 1 a 1
            limite=len(textoAPal)
            if limite>len(textoBPal):
                limite = len(textoBPal)
            for i in range(limite):
                if texto:
                    contador=contador+1
            '''
            for palabraA in textoAPal:
                if textoBPal.__contains__(palabraA):
                    contador+=1
            porcentajeSimilitud= round(float(contador)/float(len(textoAPal)),2)
            #print "cont",contador, "long", len(textoAPal),  " %", porcentajeSimilitud

            if porcentajeSimilitud>umbral and porcentajeSimilitud<1:
                print "----\n\n", textosA[contadorA]
                print porcentajeSimilitud
                print textosB[contadorB]
                nuevosTextosA.append(textosA[contadorA])
                nuevosTextosB.append(textosB[contadorB])
                relacionAB.append(porcentajeSimilitud)

            contadorB+=1
        contadorA+=1
    return nuevosTextosA, nuevosTextosB, relacionAB


#-------------------------------MAIN------------------------------------------------
notiLozano = GestorEntradasSalidas.cargarcsv("notiLozano.csv","\n")
notiLozano = notiLozano[10:1000]
notiHistorico = GestorEntradasSalidas.cargarcsv("notiHistorico.csv","\n")
notiHistorico = notiHistorico[15:3000]

'''
for n in notiLozano:
    print n, "\n"
    print " ----otro Lozano ---"

for n in notiHistorico:
    print n, "\n"
    print " ----otro Historico---"
'''
textosA, textosB, porcentajeSim = getSimilitudMorfologicaEn2CorpusTextuales(notiLozano,notiHistorico,0.6)
print "fin"
output_table = DataFrame({
        'textosA' : textosA,
        'textosB' : textosB,
        'similitud': porcentajeSim
        })
