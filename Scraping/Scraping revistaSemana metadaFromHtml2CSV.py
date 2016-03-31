#!/usr/bin/python
# -*- coding: utf-8 -*-

import timeit
from pandas import *
from urllib import *
import re
from ServiciosTecnicos.GestorEntradasSalidas import *
from AnalisisLinguistico.AnalisisMorfologico import *

'''
ini = timeit.timeit()
fin = timeit.timeit() 
print abs((fin-ini)*1000)
'''

'''
ESTE SCRIPT OBTENDRÁ TODAS LOS ARTICULOS DE UNA PAGINA WEB DE PERIODICOS LA CUAL CUMPLA CON PATRONES DE SCRAPING,
---VERSION - Revista Semana
'''
#31 marzo 2016 no saco resultados desde la web, si en htmls guardados en 2015

htmlsAll = []
#Se obtiene una muestra de htmls con noticias
myUrl ="http://www.semana.com/vida-moderna/articulo/un-tigre-una-cabra-del-zoologico-de-rusia-son-amigos/"
for i in range(201,202):
    url = myUrl+(42036).__str__()+"-3"
    print "lenyendo pagina", i*i+11
    usock = urlopen(url)
    htmlsAll.append(usock.read().decode("latin-1"))
    usock.close()


allFails = []
titulosAll = []
subTitulosAll = []
fechasAll = []
articulosAll = []

terminosInapropiados=["@", "{", "var"] #tiene hiperlinks de twiter o errores en el patron
j=1
contador=0
while contador < len(htmlsAll):
    try:
        falloUrl = False
        data = htmlsAll[contador]
        data = data.replace("\n"," ")
        # 1. OBTENGO ARTICULO Y METADATOS
        print "--------------NUEVO ARTICULO----------------"
        print contador
        pInInf = '<!DOCTYPE html>'
        pFinInf ="<!--Traffic Control-->"
        #toda info
        indiceIn=data.find(pInInf)
        indiceFin= data.find(pFinInf)
        info=data[indiceIn:indiceFin]

        print "aja e", len(info)
        print "info general:", info[0:50]

        pInTit = '<meta property="ps:title" content="'
        pFinTit = '"/>'
        pInUrl= '<meta property="ps:url" content='
        pFinUrl = '"/>'
        pInSubTit = '<meta name="description" content="'
        pFinSubTit = '"/>'

        pInFecha = '<meta property="ps:publishDate" content="'
        pFinFecha = '"/>'

        #titulo

        indiceIn=info.find(pInTit)
        tituloArt=info[indiceIn:]
        indiceFin= tituloArt.find(pFinTit)
        tituloArt=tituloArt[:indiceFin]

        tituloArt = getOcurrenciasExpresion(info,pInTit,pFinTit)[0]
        print tituloArt, "el titulo ps"
        urlArt = getOcurrenciasExpresion(info,pInUrl,pFinUrl)[0]
        # subtitulo
        ocurr = getOcurrenciasExpresion(info,pInSubTit,pFinSubTit)
        if ocurr:
            subTituloArt = ocurr[0]
        else:
            subTituloArt = "none"
        # fecha
        ocurr = getOcurrenciasExpresion(info,pInFecha,pFinFecha)
        if ocurr:
            fechaArt = ocurr[0]
        else:
            fechaArt = "none"

        #articulo
        pInArt = '<!-- Alliance -->'
        pFinArt ="<!-- Noticias Relacionadas -->"
        #toda info

        indiceIn=data.find(pInArt)
        articulo=data[indiceIn:]
        indiceFin= articulo.find(pFinArt)
        articulo=articulo[:indiceFin]

        # 2. LIMPIEZA
        # Limpiar metadatos
        tituloArt = tituloArt[len(pInTit):len(pFinTit)*-1]
        subTituloArt = subTituloArt[len(pInSubTit):len(pFinSubTit)*-1]
        fechaArt = fechaArt[len(pInFecha):len(pFinFecha)*-1]
        url = tituloArt[len(pInUrl):len(pFinUrl)*-1]

        # Limpiar articulo
        # whiteSpaces y simbolos
        articulo = deleteExpresion(articulo,"<!--","-->")
        articulo = deleteExpresion(articulo,"<",">")
        articulo = articulo.replace("#","")

        articulo = articulo.replace(chr(9),"")      # tabulador normal
        articulo = articulo.replace(chr(10),"")     # tabulador extraño
        articulo = articulo.replace(chr(13),"")     # tabulador extraño 2
        # final
        articulo = articulo.strip()
        if len(articulo)<2:
            articulo = "none"
            falloUrl = True

        titulosAll.append(tituloArt)
        subTitulosAll.append(subTituloArt)
        fechasAll.append(fechaArt)
        articulosAll.append(articulo)
        if falloUrl:
            allFails.append("mal")
        else:
            allFails.append("bien")

        # Muestro resultados limpios
        print urlArt
        #print "\n Titulo\n", tituloArt,"\n"
        #print "\n SubTitulo\n", subTituloArt,"\n"
        #print "\n Fecha: ", fechaArt, "\n"
        #print "\n articulo \n", articulo
        contador +=1
    except:
        titulosAll.append("none")
        subTitulosAll.append("none")
        fechasAll.append("none")
        articulosAll.append("none")
        allFails.append("mal")
        contador = contador+1
        continue

output_table = DataFrame({
                'Titulos' : titulosAll,
                'SubTitulos' : subTitulosAll,
                'Fecha' : fechasAll,
                'Articulos' : articulosAll,
                'fallidas' : allFails
                })
print allFails