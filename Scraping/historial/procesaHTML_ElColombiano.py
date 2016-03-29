#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib import *
from AnalisisLinguistico.AnalisisMorfologico import *

'''
ini = timeit.timeit()
fin = timeit.timeit()
print abs((fin-ini)*1000)
'''

'''
ESTE SCRIPT OBTENDRÁ TODAS LOS ARTICULOS DE UNA PAGINA WEB DE PERIODICOS LA CUAL CUMPLA CON PATRONES DE SCRAPING,
SE MUESTRA UN EJEMPLO CON LA PAGINA WEB EL_COLOMBIANO_.COM.
SOLO ES NECESARIO ESPECIFICAR LA URL Y EL TOPE (PAGINA MAX A LA QUE SE DESEA LLEGAR)
'''

#'''# NIVEL LISTAS: OBTENER TODAS LAS URL DE LAS NOTICIAS
topeInicio=1
topePag= 0
miUrl = "http://www.elcolombiano.com/busqueda/-/search/que/false/false/19150825/20150825/date/true/true/sectionName%3A*e781a51c-2d7b-4098-8ad5-d5a42f425e21*/0/meta/0/0/0/"

todasUrls = []
todasPagUrls = []
patronInicio= "</span> </div> <figure class=\"img-noticia\"> <a href=\""
patronFin=">"
tampin= len(patronInicio)
urlsCorruptas = ["ecbloguer"] # ecbloguer es un blog externo de elcolombiano.com

print "Se procesarán", topePag, "páginas..."
for i in range(topeInicio,topeInicio+topePag+1):
    print "Leyendo página", i,"..."
    url = miUrl+i.__str__()
    usock = urlopen(url)
    data = usock.read()
    data = data.decode("utf-8")
    usock.close()
    #recorto la seccion donde estan las url
    init = data.index(patronInicio)
    data = data[init:init+10000]
    listaE= getOcurrenciasExpresion(data,patronInicio,patronFin)
    #obtengo las url
    for url in listaE:
        inapropiado = getOcurrenciasExpresiones(url,urlsCorruptas)
        if inapropiado <> []:
            continue
        url=url[tampin:-2]
        url= "http://www.elcolombiano.com"+url
        todasUrls.append(url)
        todasPagUrls.append(i)





#''' # NIVEL DE ARTICULO: OBTENER EL PARRAFO DE LA NOTICIA DEL ARTICULO

nombreArchivoUrls = str(topePag)+"Url.txt"
outputUrl=open(nombreArchivoUrls,"w")
outputUrl.close()   # Reinicio txt
outputUrl = open(nombreArchivoUrls,"a")

nombreArchivo = str(topePag)+"Art.txt"
outputArt=open(nombreArchivo,"w")
outputArt.close()
outputArt = open(nombreArchivo,"a")

terminosInapropiados=["@","&nbsp"] #tiene hiperlinks de twiter o errores en el patron

#PATRONES DE EXTRACCION DE INFORMACION

#notese que inInfo es == inicio titulo y finInfo == finArticulo
pInInf = '<div class="information-noticia"> <h3>'
pFinInf = "</article>"

pInTit = '<div class="information-noticia"> <h3>'
pFinTit = '</h3>'

pInTags = '<a class ="categoryListItemLink" href='
pFinTags= ">"

pInAutorFecha = '<div class="autor"> <h6>'
pFinAutorFecha = '</h6>'

pInArt = "<!-- cxenseparse_start -->"
pFinArt = "</article>"

j=1
cantidadArt=0
for url in todasUrls:
    # 1. OBTENGO ARTICULO Y METADATOS
    usock = urlopen(url)
    data = usock.read()
    # data = data.decode("utf-8") se usa en knime
    usock.close()
    print "tyData ", type(data)

    #toda info
    indiceIn=data.find(pInInf)
    indiceFin= data.find(pFinInf)
    info=data[indiceIn:indiceFin]

    # titulo
    indiceIn=info.find(pInTit)
    indiceFin= info.find(pFinTit)
    tituloArt=info[indiceIn:indiceFin]

    # tags
    tagsArt =  getOcurrenciasExpresion(info,pInTags,pFinTags)

    # autor y fecha
    indiceIn=info.find(pInAutorFecha)
    indiceFin= info.find(pFinAutorFecha)
    autorFechaArt=info[indiceIn:indiceFin]

    # articulo
    indiceIn=info.find(pInArt)
    indiceFin= info.find(pFinArt)
    articulo=info[indiceIn:indiceFin]

    # mover para antesito del for (ver elTiempo)
    print "--------ARTICULO NUEVO ----------", j, "pagina", todasPagUrls[j-1]
    print url
    j=j+1

    # 2. LIMPIO ARTICULO Y METADATOS

    # limpio titulo
    tituloArt = deleteExpresion(tituloArt,"<",">")
    tituloArt = tituloArt.strip()

    # nada que limpiar en tags...

    #limpio autor y fecha
    autorFechaArt = deleteExpresion(autorFechaArt,"<",">")
    autorFechaArt = autorFechaArt.replace("|", "")
    autorFechaArt = " ".join(autorFechaArt.split())
    autorFechaArt = autorFechaArt.split("Publicado el")
    if len(autorFechaArt)>1:
        autorArt= autorFechaArt[0]
        fechaArt = autorFechaArt[1]
    # aveces el autor no aparece o aparece con otro patron, la fecha siempre
    else:
        autorArt = ""
        fechaArt = autorFechaArt[0]

    # Limpio articulo
    # whiteSpaces y simbolos
    articulo = articulo.replace("\n"," ")
    articulo = deleteExpresion(articulo,"<",">")
    articulo = articulo.replace("”"," ' ")
    articulo = articulo.replace("“"," ' ")
    articulo = articulo.replace("‘"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace("—","")
    articulo = articulo.replace("#","")
    articulo = re.sub('[\t]+' , ' ', articulo)
    articulo = articulo.strip()

    # cortar si encontro codigo en medio del patron.
    articuloVector = str(articulo).split()
    indiceTerminosInapropiados = getIndicesPalabrasClavesOR(articuloVector,terminosInapropiados)

    if indiceTerminosInapropiados <> []:
        print "--RECORTADO-- En este articulo encontro uno de los sgts terminos inapropiados", indiceTerminosInapropiados
        articuloVector = articuloVector[0:min(indiceTerminosInapropiados)]
        articulo = vector2paragraph(articuloVector)

    # Muestro resultados limpios
    print "\n Titulo\n", tituloArt,"\n"
    print "\n tags\n",tagsArt,"\n"
    print "\n Autor: ",autorArt,"\n", "Fecha: ", fechaArt, "\n"
    print "\n articulo \n", articulo



    # 3. ALMACENO EL ARTICULO Y METADATOS
    outputArt.write(articulo+" # ")
    if cantidadArt <>0: #primera iteracion
        outputUrl.write(",")
    outputUrl.write(url)
    cantidadArt+=1
outputArt.close()
outputUrl.close()
print "\n ",cantidadArt, "articulos salvados en","'"+nombreArchivo+"'", "\nLas urls las puedes encontrar en","'"+nombreArchivoUrls+"'"
#''' # FIN  NIVEL ARTICULO

#se hizo optimizacion de tiempos
# salidas en archivos de compatibilidad
# informe de procesos realizados por consola



# Guardar conjunto de htmls (completos)