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
---VERSION -
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

htmlsAll = []

urls = []
urls.append("http://www.procuraduria.gov.co/portal/Mediante-fallo_de_segunda_instancia__destituido_exdiputado_del_Quindio.news")
urls.append("http://www.procuraduria.gov.co/portal/Procuraduria-General-de-la-Nacion-formulo-cargos-a-docente-de-Institucion-Educativa-INEM-de-Ibague_-Tolima.news")
urls.append("http://www.procuraduria.gov.co/portal/Procuraduria-General_de_la_Nacion_formul__recomendaciones_ante_problematica_que_enfrenta_el_pa_s_por_incendios_forestales.news")
for url in urls:
    usock = urlopen(url)
    htmlsAll.append(usock.read().decode("latin-1"))
    usock.close()

allFails = []
titulosAll = []
subTitulosAll = []
autoresAll = []
fechasAll = []
articulosAll = []

terminosInapropiados=[] #tiene hiperlinks de twiter o errores en el patron
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



        # patrones toda info
        pInInf = '<div class="news-view">'
        pFinInf ='<div id="footer">'
        # patrones metadatos
        pInTit = '<h2 class="prueba">'
        pFinTit = '</h2>'
        pInSubTit = 'subtitle">'
        pFinSubTit = '</'
        pInAutor = '>Fuente:'
        pFinAutor = '<'
        pInFecha = 'Fecha Publicaci&oacute;n:'
        pFinFecha = '</'
        pInArt = 'style="font-size:'

        pFinArt = pFinInf

        #toda info
        indiceIn=data.find(pInInf)
        indiceFin= data.find(pFinInf)
        info=data[indiceIn:indiceFin]
        #titulo
        tituloArt = getOcurrenciasExpresion(info,pInTit,pFinTit)[0]
        # subtitulo
        ocurr = getOcurrenciasExpresion(info,pInSubTit,pFinSubTit)
        if ocurr:
            subTituloArt = ocurr[0]
        else:
            subTituloArt = "none"
        # autor
        autorArt = getOcurrenciasExpresion(info,pInAutor,pFinAutor)[0]
        # fecha
        ocurr = getOcurrenciasExpresion(info,pInFecha,pFinFecha)
        if ocurr:
            fechaArt = ocurr[0]
        else:
            fechaArt = "none"
        #articulo
        indiceIn=data.find(pInArt)
        articulo=data[indiceIn:]
        indiceFin= articulo.find(pFinArt)
        articulo=articulo[:indiceFin]

        # 2. LIMPIEZA
        # Limpiar metadatos
        tituloArt = tituloArt[len(pInTit):len(pFinTit)*-1]
        subTituloArt = subTituloArt[len(pInSubTit):len(pFinSubTit)*-1]
        autorArt = autorArt[len(pInAutor):len(pFinAutor)*-1]
        fechaArt = fechaArt[len(pInFecha):len(pFinFecha)*-1].strip()

        # Limpiar articulo
        # whiteSpaces y simbolos
        articulo = deleteExpresion(articulo,"<!--","-->")
        articulo = deleteExpresion(articulo,"<",">")
        articulo = articulo.replace('12px" align="justify">',"")
        articulo = articulo.replace('12px">',"")
        articulo = articulo.replace(chr(9),"")      # tabulador normal
        articulo = articulo.replace(chr(10),"")     # tabulador extraño
        articulo = articulo.replace(chr(13),"")     # tabulador extraño 2
        articulo = articulo[len(pInArt):]
        # final
        articulo = articulo.strip()
        if len(articulo)<2:
            articulo = "none"
            falloUrl = True

        titulosAll.append(tituloArt)
        subTitulosAll.append(subTituloArt)
        autoresAll.append(autorArt)
        fechasAll.append(fechaArt)
        articulosAll.append(articulo)

        if falloUrl:
            allFails.append("mal")
        else:
            allFails.append("bien")

        # Muestro resultados limpios
        print "\n Titulo\n", tituloArt,"\n"
        print "\n SubTitulo\n", subTituloArt,"\n"
        print "\n Fecha:", fechaArt, "\n"
        print "\n articulo \n", articulo
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