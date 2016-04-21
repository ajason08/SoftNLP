#!/usr/bin/python
# -*- coding: utf-8 -*-

#INSTRUCCIONES knime:
# eliminar las lineas referentes al utf-8 (primeras dos)

import timeit
from pandas import *
import re
from urllib import *
#from ServiciosTecnicos.GestorEntradasSalidas import *
#from AnalisisLinguistico.AnalisisMorfologico import *


'''
ini = timeit.timeit()
fin = timeit.timeit()
print abs((fin-ini)*1000)
'''

'''
NIVEL DE ARTICULO: OBTENER metadatos DE LA NOTICIA
---VERSION - NCTC
'''
#Se obtiene una muestra de htmls con noticias

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


def scrapingForCaptured(data):
    falloUrl = False
    # patrones info general
    pInInfNombre = '<!-- InstanceBeginEditable name="CapKillName" -->'
    pFinInfNombre ='<!-- InstanceEndEditable -->'

    pInEstadoDescripcion = '<!--STATS -->'
    pFinEstadoDescripcion ='<!--END STATS-->'

    # patrones metadatos
    pInNombre = '<h2 class="shorter">'
    pFinNombre = '</h2>'

    pInEstado = 'alt="'
    pFinEstado = '"></div>'
    pInDescripcion = '<p class="smallcaps">'
    pFinDescripcion = '</p>'

    # infogeneral
    infoNombre = getOcurrenciasExpresion(data,pInInfNombre,pFinInfNombre)[0]
    infoEstadoDescripcion= getOcurrenciasExpresion(data,pInEstadoDescripcion,pFinEstadoDescripcion)[0]
    #nombre
    nombre = getOcurrenciasExpresion(infoNombre,pInNombre,pFinNombre)[0]
    # estado
    ocurr = getOcurrenciasExpresion(infoEstadoDescripcion,pInEstado,pFinEstado)
    if ocurr:
        estado = ocurr[0]
    else:
        estado = "none"
    # despcripcion
    descripcion = getOcurrenciasExpresion(infoEstadoDescripcion,pInDescripcion,pFinDescripcion)[0]

    # 2. LIMPIEZA
    # Limpiar metadatos
    nombre = nombre[len(pInNombre):len(pFinNombre)*-1]
    estado = estado[len(pInEstado):len(pFinEstado)*-1]
    descripcion = descripcion.replace("\r"," ")
    descripcion = deleteExpresion(descripcion,"<",">")
    descripcion = descripcion.strip()

    nombresAll.append(nombre)
    estadosAll.append(estado)
    descripcionAll.append(descripcion)

    if falloUrl:
        allFails.append("mal")
    else:
        allFails.append("bien")

    # Muestro resultados limpios
    print "\n nombre\n", nombre,"\n"
    print "\n estado\n", estado,"\n"
    print "\n descripcion:", descripcion, "\n"


def scrapingForBuscado(data):
    falloUrl = False
    # patrones info general
    pInInfNombre = '<!-- InstanceBeginEditable name="Profile" -->'
    pFinInfNombre ='<!-- InstanceEndEditable -->'

    pInNombre = 'alt="'
    pFinNombre = '"'

    pInDescripcion = '<!-- InstanceBeginEditable name="ProfieText" -->'
    pFinDescripcion = '<!-- InstanceEndEditable -->'

    # infogeneral
    infoNombre = getOcurrenciasExpresion(data,pInInfNombre,pFinInfNombre)[0]

    #nombre
    nombre = getOcurrenciasExpresion(infoNombre,pInNombre,pFinNombre)[0]
    # estado
    estado= "Wanted"
    # despcripcion
    descripcion = getOcurrenciasExpresion(data,pInDescripcion,pFinDescripcion)[0]
    descripcion = descripcion.replace("\r"," ")
    descripcion = deleteExpresion(descripcion,"<",">")
    descripcion = descripcion.strip()
    # 2. LIMPIEZA
    # Limpiar metadatos
    nombre = nombre[len(pInNombre):len(pFinNombre)*-1]
    descripcion = descripcion[len(pInDescripcion):len(pFinDescripcion)*-1]

    nombresAll.append(nombre)
    estadosAll.append(estado)
    descripcionAll.append(descripcion)

    if falloUrl:
        allFails.append("mal")
    else:
        allFails.append("bien")

    # Muestro resultados limpios
    print "\n nombre\n", nombre,"\n"
    print "\n estado\n", estado,"\n"
    print "\n descripcion:", descripcion, "\n"

htmlsAll = []
caracteristicas= []
caracteristicas.append("x")
caracteristicas.append("x")
caracteristicas.append("none")
caracteristicas.append("none")

# obtengo una muestra de urls
urls = []
urls.append("https://www.nctc.gov/site/profiles/abdelbasit_hamad.html")
urls.append("https://www.nctc.gov/site/profiles/ayman_al_zawahiri.html")
urls.append("https://www.nctc.gov/site/profiles/abd_al_hadi_al_iraqi.html")
urls.append("https://www.nctc.gov/site/profiles/abu_khabab_al_masri.html")
for url in urls:
    usock = urlopen(url)
    htmlsAll.append(usock.read().decode("latin-1"))
    usock.close()

allFails = []
nombresAll = []
estadosAll = []
descripcionAll = []

terminosInapropiados=[] #tiene hiperlinks de twiter o errores en el patron
j=1
contador=0
while contador < len(htmlsAll):
    try:
        data = htmlsAll[contador]
        data = data.replace("\n"," ")
        # 1. OBTENGO ARTICULO Y METADATOS
        print "--------------NUEVO ARTICULO----------------"
        print contador

        if caracteristicas[contador]=="none":
            scrapingForCaptured(data)
        else:
            scrapingForBuscado(data)
        contador +=1
    except:
        nombresAll.append("none")
        estadosAll.append("none")
        descripcionAll.append("none")
        allFails.append("mal")
        contador = contador+1
        continue

output_table = DataFrame({
                'Nombre' : nombresAll,
                'Estado' : estadosAll,
                'Descripcion' : descripcionAll,
                'fallidas' : allFails
                })
print allFails