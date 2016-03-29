#!/usr/bin/python
# -*- coding: utf-8 -*-

#INSTRUCCIONES:
# eliminar las lineas referentes al utf-8 (primeras dos)
# si se descomenta el import future...
    # lo bueno: se pueden hacer los reemplazos incluyendo simbolos
    # lo malo: trae problemas inesperados, obliga que todos sea unicode siempre.
    # solucion: no usarlo, los reemplazos se pueden ahcer en knime (jsnipet)
# descomentar el comment que menciona -se usa en knime-
# quitar instruccion exit antes del dataframe

#from __future__ import unicode_literals
import timeit
from pandas import *
import re
from urllib import *
from ServiciosTecnicos.GestorEntradasSalidas import *
from AnalisisLinguistico.AnalisisMorfologico import *

'''
ini = timeit.timeit()
fin = timeit.timeit()
print abs((fin-ini)*1000)
'''

'''
ESTE SCRIPT OBTENDRÁ TODAS LOS ARTICULOS DE UNA PAGINA WEB DE PERIODICOS LA CUAL CUMPLA CON PATRONES DE SCRABING,

---VERSION - EL TIEMPO
Se deeben tener en cuenta las siguientes consideraciones:
La pagina del tiempo parece vigilar los accesos, cancelando el ingreso de la ip cuando son demasiado frecuentes
A nivel de articulo el tiempo presenta diferentes tipos de codificacion de sus articulos, por ej. desde que usa html ya no imprime tildes
A nivel de articulo el tiempo presenta diferentes patrones de inicio y final a partir aprox de marzo 2014, el cambio es difuso.
A nivel de articulo el patron de inicio y final parece mantenerse desde el inicio del periodico hasta el 2013
'''

htmlsAll = cargarcsv("D:\Usuario\Desktop\outSampling2.csv", "$#$")

# NIVEL DE ARTICULO: OBTENER EL PARRAFO DE LA NOTICIA DEL ARTICULO


allFails = []
titulosAll = []
subTitulosAll = []
autoresAll = []
fechasAll = []
articulosAll = []

terminosInapropiados=["@", "{", "var"] #tiene hiperlinks de twiter o errores en el patron

j=1
contador=0
while contador < len(htmlsAll):
    try:
        falloUrl = False
        data = htmlsAll[contador]

        # 1. OBTENGO ARTICULO Y METADATOS
        # notese que inInfo es == inicio titulo y finInfo == finArticulo
        print "--------------NUEVO ARTICULO----------------"
        print contador
        patron = "nulo"


        # Primer tipo de patrones
        pInInf = '<hgroup>'
        pFinInf ='</p>.*?</div>'
        #toda info

        indiceIn=data.find(pInInf)
        indiceFin= data.find(pFinInf)
        info=data[indiceIn:indiceFin]
        info = info.replace("\n"," ")

        if len(info)>1:
            pInTit = pInInf
            pFinTit = '</h1>'

            pInSubTit = '<h2'
            pFinSubTit = '</h2>'

            pInAutor = '"author">'
            pFinAutor = '<.*?>'

            pInFecha = ';</span>'
            pFinFecha = '</time>'

            pInArt1 = '<div id="contenido">'
            pFinArt1 = pFinInf
            pInArt2 = '<div class="columna_articulo">'
            pFinArt2 = pFinInf

        #titulo
        tituloArt = getOcurrenciasExpresion(info,pInTit,pFinTit)[0]
        # subtitulo
        ocurr = getOcurrenciasExpresion(info,pInSubTit,pFinSubTit)
        if ocurr:
            subTituloArt = ocurr[0]
        else:
            subTituloArt = "none"
        # autor
        ocurr = getOcurrenciasExpresion(info,pInAutor,pFinAutor)
        if ocurr:
            autorArt = ocurr[0]
        else:
            autorArt = "none"
        # fecha
        ocurr = getOcurrenciasExpresion(info,pInFecha,pFinFecha)
        if ocurr:
            fechaArt = ocurr[0]
        else:
            fechaArt = "none"

        # articulo
        ocurr = getOcurrenciasExpresion(info,pInArt1,pFinArt1)
        if ocurr:
            articulo = ocurr[0]
        else:
            ocurr = getOcurrenciasExpresion(info,pInArt2,pFinArt2)
        if ocurr:
            articulo = ocurr[0]
        else:
            falloUrl = True
            articulo = "none"


        # 2. LIMPIEZA
        # Limpiar metadatos
        #tituloArt = tituloArt[len(pInTit):]
        tituloArt = deleteExpresion(tituloArt,"<",">").strip()
        subTituloArt = deleteExpresion(subTituloArt,"<",">").strip()
        autorArt = deleteExpresion(autorArt,"<",">").strip()
        autorArt = deleteDuplicateString(autorArt)
        fechaArt = deleteExpresion(fechaArt,"<",">").strip()

        # Limpiar articulo
        # whiteSpaces y simbolos
        articulo = deleteExpresion(articulo,"<!--","-->")
        articulo = deleteExpresion(articulo,"<",">")
        articulo = articulo.replace("#","")
        #comillas
        #articulo = articulo.replace("”"," ' ")
        #articulo = articulo.replace("“"," ' ")
        #articulo = articulo.replace("‘"," ' ")
        #articulo = articulo.replace("’"," ' ")
        #articulo = articulo.replace("’"," ' ")
        #articulo = articulo.replace('"'," ' ")
        # codificacion html
        #articulo = articulo.replace("&aacute;","á")
        #articulo = articulo.replace("&eacute;","é")
        #articulo = articulo.replace("&iacute;","í")
        #articulo = articulo.replace("&oacute;","ó")
        #articulo = articulo.replace("&uacute;","ú")
        #articulo = articulo.replace("&ntilde;","ñ")
        #articulo = articulo.replace("&uuml;","ü")
        #articulo = articulo.replace("&Aacute;","Á")
        #articulo = articulo.replace("&Eacute;","É")
        #articulo = articulo.replace("&Iacute;","Í")
        #articulo = articulo.replace("&Oacute;","Ó")
        #articulo = articulo.replace("&Uacute;","Ú")
        #articulo = articulo.replace("&Ntilde;","Ñ")
        #articulo = articulo.replace("&Uuml;","Ü")
        #articulo = articulo.replace("&iquest;","¿")
        #articulo = articulo.replace("&nbsp;"," ")
        #articulo = articulo.replace("&ldquo;"," ' ")
        #articulo = articulo.replace("&rdquo;"," ' ")
        #articulo = articulo.replace("&lsquo;"," ' ")
        #articulo = articulo.replace("&rsquo;"," ' ")
        #articulo = articulo.replace("&iexcl;"," ¡ ")
        #articulo = articulo.replace("&deg;"," ° ")
        #articulo = articulo.replace("&ndash;"," - ")
        #articulo = articulo.replace("&ordf;"," ")
        # casos especiales
        #articulo = articulo.replace("—","")
        articulo = articulo.replace(chr(9),"")      # tabulador normal
        articulo = articulo.replace(chr(10),"")     # tabulador extraño
        articulo = articulo.replace(chr(13),"")     # tabulador extraño 2
        # final
        articulo = articulo.strip()

        # 2.1 cortar si encontro codigo en medio del patron, fue codificado por precausion, nunca lo he usado.
        #articuloVector = str(articulo).split()
        #indiceTerminosInapropiados = getIndicesPalabrasClavesOR(articuloVector,terminosInapropiados)
        #if indiceTerminosInapropiados <> []:
            #print "--RECORTADO-- En este articulo encontro uno de los sgts terminos inapropiados", indiceTerminosInapropiados
            #articuloVector = articuloVector[0:min(indiceTerminosInapropiados)]
            #articulo = vector2paragraph(articuloVector)

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
        #print "\n Titulo\n", tituloArt,"\n"
        #print "\n SubTitulo\n", subTituloArt,"\n"
        #print "\n Autor: ",autorArt,"\n"
        #print "\n Fecha: ", fechaArt, "\n"
        #print "\n articulo \n", articulo
        #print "\n articulo \n", articulo

        #print "\n htmls\n", len(htmlsAll),"\n"
        #print "\n tits: ",len(titulosAll),"\n"
        #print "\n subs: ", len(subTitulosAll), "\n"
        #print "\n autores \n", len(autoresAll)
        #print "\n fechas \n", len(fechasAll)
        #print "\n articulos \n", len(articulosAll)
        contador +=1
    except:
        titulosAll.append("none")
        subTitulosAll.append("none")
        autoresAll.append("none")
        fechasAll.append("none")
        articulosAll.append("none")
        allFails.append("mal")
        contador = contador+1
        continue

output_table = DataFrame({
                'Titulos' : titulosAll,
                'SubTitulos' : subTitulosAll,
                'Autores' : autoresAll,
                'Fecha' : fechasAll,
                'Articulos' : articulosAll,
                'fallidas' : allFails
                })
print allFails

#print output_table.get_value(output_table.index[0],'Fecha')

#exportarExcel(output_table)
#exportarMatrizCSV(output_table, "NoticiasElTiempoFromHTMLs"+".csv")
#print list(output_table.columns.values)
#print len(output_table.axes[0])
#print len(output_table.axes[1])

