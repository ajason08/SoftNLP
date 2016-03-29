#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib import *

from AnalisisLinguistico.AnalisisMorfologico import *

'''
ESTE SCRIPT OBTENDRÁ TODAS LOS ARTICULOS DE UNA PAGINA WEB DE PERIODICOS LA CUAL CUMPLA CON PATRONES DE SCRAPING,
---VERSION - Fiscalia.gov.co
'''


'''
ini = timeit.timeit()
fin = timeit.timeit()
print abs((fin-ini)*1000)
'''
#'''# NIVEL LISTAS: OBTENER TODAS LAS URL DE LAS NOTICIAS
topeInicio=1000
topePag=500
print "Se procesarán", topePag, "páginas..."
todasUrls = []
todasPagUrls = []
urlsCorruptas = ["ecbloguer"] # ecbloguer es un blog externo de elcolombiano.com


patronInicio= '<div class="big">'
patronFin="</div> <!-- /big -->"
patronInicio2='<a class="titulo-noticia-home" href="'
patronFin2='"'

for i in range(topeInicio,topeInicio+topePag):
    print "Leyendo página", i,"..."
    url = "http://www.fiscalia.gov.co/colombia/todas-las-noticias/page/"+i.__str__()
    print "listado", url
    usock = urlopen(url)
    data = usock.read()
    usock.close()
    #recorto la seccion donde estan las url
    init = str(data).index(patronInicio)
    data = data[init:init+15000]

    listaE= getOcurrenciasExpresion(data,patronInicio2,patronFin2)
    #obtengo urls limpias
    listaE =getUniqs(listaE)
    for url in listaE:
        inapropiado = getOcurrenciasExpresiones(url,urlsCorruptas)
        if inapropiado <> []:
            print "--DESCARTADO-- Se encontro:", inapropiado
            continue
        url = url[len(patronInicio2):len(patronFin2)*-1]
        #print "mi url", url
        #url= "http:"+url
        todasUrls.append(url)
        todasPagUrls.append(i)
        #print url, "\n"*2









# NIVEL DE ARTICULO: OBTENER EL PARRAFO DE LA NOTICIA DEL ARTICULO
nombreArchivoUrls = str(topePag)+"Url.txt"
outputUrl=open(nombreArchivoUrls,"w")
outputUrl.close()   # Reinicio txt
outputUrl = open(nombreArchivoUrls,"a")

nombreArchivo = str(topePag)+"Art.txt"
outputArt=open(nombreArchivo,"w")
outputArt.close()   # Reinicio txt
outputArt = open(nombreArchivo,"a")

terminosInapropiados=["@", "{", "var"] #tiene hiperlinks de twiter o errores en el patron
patronIn = '<div id="content">'
patronFin = '<p>&nbsp;</p>'
j=1
cantidadArt=0
for url in todasUrls:
    #obtengo articulo
    usock = urlopen(url)
    data = usock.read()
    usock.close()
    indiceIn=data.find(patronIn)
    indiceFin= data.find(patronFin)
    articulo=data[indiceIn:indiceFin]

    #determino si el articulo es valido
    print "--------ARTICULO NUEVO ----------", j, "pagina", todasPagUrls[j-1]
    print url
    j=j+1

    # Si el primer patron falla intento con el segundo
    if len(articulo)<2:
        print "--DESCARTADO-- No se encontro el articulo"
        continue

    # accion inicial de limpieza: cortar si encontro codigo en medio del patron.
    articuloVector = str(articulo).split()
    indiceTerminosInapropiados = getIndicesPalabrasClavesOR(articuloVector,terminosInapropiados)
    if indiceTerminosInapropiados <> []:
        print "--RECORTADO-- En este articulo encontro uno de los sgts terminos inapropiados", indiceTerminosInapropiados
        articuloVector = articuloVector[0:min(indiceTerminosInapropiados)]
    #probar meterlo dentro del if
    articulo = vector2paragraph(articuloVector)


    # limpio (whiteSpaces y simbolos) y almaceno el articulo
    articulo = articulo.replace("\n"," ")
    articulo = deleteExpresion(articulo,"<!--","-->")
    articulo = deleteExpresion(articulo,"<",">")

    articulo = articulo.replace("”"," ' ")
    articulo = articulo.replace("“"," ' ")
    articulo = articulo.replace("‘"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace('"'," ' ")

    articulo = articulo.replace("—","")
    articulo = articulo.replace("#","")



    articulo = articulo.replace(chr(9),"")      # tabulador normal
    articulo = articulo.replace(chr(10),"")     # tabulador extraño
    articulo = articulo.replace(chr(13),"")     # tabulador extraño 2
    articulo = articulo.strip()

    print articulo


    outputArt.write(articulo+" # ")
    if cantidadArt <>0: #primera iteracion
        outputUrl.write(",")
    outputUrl.write(url)
    cantidadArt+=1
outputArt.close()
outputUrl.close()
print "\nRESULTADO: ",cantidadArt, "articulos salvados en","'"+nombreArchivo+"'", "\nLas urls las puedes encontrar en","'"+nombreArchivoUrls+"'"
# FIN  NIVEL ARTICULO

#se hizo optimizacion de tiempos
# salidas en archivos de compatibilidad
# informe de procesos realizados por consola