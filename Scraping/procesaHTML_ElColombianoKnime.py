#!/usr/bin/python
# -*- coding: utf-8 -*-

#INSTRUCCIONES:
# eliminar las lineas referentes al utf-8 (primeras dos)
# descomentar el comment que menciona -se usa en knime-
# quitar instruccion exit antes del dataframe
# quitar los prints necesarios
# bug : se debe quitar ademas los replace de comillas
# y to-do lo de terminos inapropiados.




from pandas import *
import re
from urllib import *

def deleteExpresion(texto, patronInicio, patronFin):
    # retorna texto sin la expresion
    patron = patronInicio+".*?"+patronFin
    cleanr =re.compile(patron)
    cleantext = re.sub(cleanr,'', texto)
    return cleantext

def getOcurrenciasExpresion(texto, patronInicio, patronFin):
    # retorna una lista con las ocurrencias del patron
    expresion = patronInicio+".*?"+patronFin
    listaE =re.findall(expresion,texto)
    return listaE

def getOcurrenciasExpresiones(texto,expresiones):
    # retorna la lista con las ocurrencias de los patrones
    listaE = []
    for expresion in expresiones:
        listaE = listaE +re.findall(expresion,texto)
    return listaE

def getIndicesPalabrasClavesOR(vector, keywords):
    #obtiene los indices donde se encuentran ciertas palabras claves en un vector. El orden de las palabras no es secuencial
    indices= []
    for i in range(len(vector)):
        for j in range(len(keywords)):
            if vector[i]==keywords[j]:
                indices.append(i)
    return indices

def vector2paragraph(vector):
    return " ".join(vector)


'''
ini = timeit.timeit()
fin = timeit.timeit()
print abs((fin-ini)*1000)
'''

#'''# NIVEL LISTAS: OBTENER TODAS LAS URL DE LAS NOTICIAS
topeInicio=1
topePag= 0
miUrl = "http://www.elcolombiano.com/busqueda/-/search/que/false/false/19150825/20150825/date/true/true/sectionName%3A*e781a51c-2d7b-4098-8ad5-d5a42f425e21*/0/meta/0/0/0/"

urlsAll = []
todasPagUrls = []
patronInicio= "</span> </div> <figure class=\"img-noticia\"> <a href=\""
patronFin=">"
tampin= len(patronInicio)
urlsCorruptas = ["ecbloguer"] # ecbloguer es un blog externo de elcolombiano.com

#print "Se procesaran", topePag, "paginas..."
for i in range(topeInicio,topeInicio+topePag+1):
    print "Leyendo pagina", i,"..."
    url = miUrl+i.__str__()
    usock = urlopen(url)
    data = usock.read()
    data = data.decode("utf-8")
    usock.close()
    print type(data)
    #exit()
    #recorto la seccion donde estan las url
    init = data.index(patronInicio)
    data = data[init:init+10000]
    listaE= getOcurrenciasExpresion(data,patronInicio,patronFin)
    #obtengo las url
    for url in listaE:
        inapropiado = getOcurrenciasExpresiones(url,urlsCorruptas)
        if inapropiado:
            continue
        url=url[tampin:-2]
        url= "http://www.elcolombiano.com"+url
        urlsAll.append(url)
        todasPagUrls.append(i)





# NIVEL DE ARTICULO: OBTENER EL PARRAFO DE LA NOTICIA DEL ARTICULO
HTMLsAll = []
titulosAll = []
tagsAll = []
autoresAll = []
fechasAll = []
articulosAll = []


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
for url in urlsAll:
    print "--------ARTICULO NUEVO ----------", j, "pagina", todasPagUrls[j-1]
    print url
    j=j+1

    # Html completo
    usock = urlopen(url)
    data = usock.read()
    #data = data.decode("utf-8") se usa en knime
    usock.close()

    # 1. OBTENGO ARTICULO Y METADATOS

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

    # 2. LIMPIEZA: METADATOS Y ARTICULO

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

    # si existe algun termino inapropiado
    if indiceTerminosInapropiados:
        print "--RECORTADO-- Se encontro uno de los sgts terminos inapropiados", indiceTerminosInapropiados
        articuloVector = articuloVector[0:min(indiceTerminosInapropiados)]
        articulo = vector2paragraph(articuloVector)

    # Agrego a la lista informacion limpia
    HTMLsAll.append(data)
    titulosAll.append(tituloArt)
    tagsAll.append(tagsArt)
    autoresAll.append(autorArt)
    fechasAll.append(fechaArt)
    articulosAll.append(articulo)

    # Muestro resultados limpios
    print "\n Titulo\n", tituloArt,"\n"
    print "\n tags\n",tagsArt,"\n"
    print "\n Autor: ",autorArt,"\n", "Fecha: ", fechaArt, "\n"
    print "\n articulo \n", articulo


output_table = DataFrame({
                'Htmls' : HTMLsAll,
                'urls' : urlsAll,
                'titulos' : titulosAll,
                'tags' : tagsAll,
                'autores' : autoresAll,
                'fecha' : fechasAll,
                'articulo' : articulosAll
                })
