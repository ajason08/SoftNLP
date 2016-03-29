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



#'''# NIVEL LISTAS: OBTENER TODAS LAS URL DE LAS NOTICIAS
#topeInicio=297
topeInicio=1
topePag= 497

urlsAll = []
todasPagUrls = []
urlsCorruptas = [] # aqui patrones detectados para saltarse url

patronInicio= "                <time"
patronInicio2="href=\"http:"
patronFin2='">'
myUrl = "http://www.eltiempo.com/archivo/buscar?q=+&producto=eltiempo&seccion=26&pagina="
print "Se procesaran", topePag, "paginas..."
for i in range(topeInicio,topeInicio+topePag+1):
    print "Leyendo pagina", i,"..."
    url = myUrl+i.__str__()+"&a=2014"
    print "listado", url
    usock = urlopen(url)
    data = usock.read()
    data = data.decode("latin-1")
    usock.close()
    #recorto la seccion donde estan las url
    init = data.index(patronInicio)
    data = data[init:init+10000]

    listaE= getOcurrenciasExpresion(data,patronInicio2,patronFin2)
    #obtengo urls limpias
    listaE =getUniqs(listaE)
    for url in listaE:
        inapropiado = getOcurrenciasExpresiones(url,urlsCorruptas)
        if inapropiado <> []:
            print "--DESCARTADO-- Se encontro:", inapropiado
            continue
        url = url[len(patronInicio2):len(patronFin2)*-1]
        url= "http:"+url
        urlsAll.append(url)
        todasPagUrls.append(i)


# NIVEL DE ARTICULO: OBTENER EL PARRAFO DE LA NOTICIA DEL ARTICULO
HTMLsAll = []
titulosAll = []
subTitulosAll = []
autoresAll = []
fechasAll = []
articulosAll = []


terminosInapropiados=["@", "{", "var"] #tiene hiperlinks de twiter o errores en el patron

j=1
contador=0
while contador < len(urlsAll):
    url = urlsAll[contador]
    print "-------- ARTICULO NUEVO ----------", j, "pagina", todasPagUrls[j-1]
    print url
    j=j+1
    # HTML completo
    usock = urlopen(url)
    data = usock.read()
    #data = data.decode('unicode-escape') #se usa en knime
    usock.close()

    # 1. OBTENGO ARTICULO Y METADATOS
    # notese que inInfo es == inicio titulo y finInfo == finArticulo

    # Primer tipo de patrones
    pInInf = 'itemprop="headline">'
    pFinInf = '</p>                    </div>'

    pInTit = pInInf
    pFinTit = '</h1>'

    pInSubTit = '<h2 itemprop="description">'
    pFinSubTit = '</h2>'

    pInAutor = '<a rel="author"'
    pFinAutor = '</a>'

    pInFecha = '&#xe01b;</span>'
    pFinFecha = '</time>'

    pInArt1 = '<div id="contenido">'
    pFinArt1 = pFinInf

    #toda info
    indiceIn=data.find(pInInf)
    indiceFin= data.find(pFinInf)
    info=data[indiceIn:indiceFin]

    # Si no se recupera info con el primer patron, intento con el segundo
    esPatron2 = False
    falloPatron = len(info)<2
    if falloPatron:
        # Segundo tipo de patrones
        pInInf = '<hgroup>'
        pFinInf = '</p>                    </div>'

        pInTit = pInInf
        pFinTit = '</h2>'

        pInSubTit = 'itemprop="description">'
        pFinSubTit = '</p>'

        pInAutor = 'data-real-type="image" alt="' #no es unico en data pero si en info
        pFinAutor = '"'

        pInFecha = '></span><span class="ico-time"></span>'
        pFinFecha = '</time>'

        pInArt1 = '<div id="contenido">'
        pFinArt1 = pFinInf

        #toda info
        indiceIn=data.find(pInInf)
        indiceFin= data.find(pFinInf)
        info=data[indiceIn:indiceFin]

        falloPatron = len(info)<2
        if falloPatron:
            print "--DESCARTADO-- No se encontro el articulo"
            urlsAll.remove(url)
            continue
        print "-------- ARTICULO NUEVO Encontrado con PATRON 2 --------"
        esPatron2 = True


    # titulo
    indiceIn=info.find(pInTit)
    indiceFin= info.find(pFinTit)
    tituloArt=info[indiceIn:indiceFin]

    # subtitulo
    indiceIn=info.find(pInSubTit)
    indiceFin= info.find(pFinSubTit)
    subTituloArt=info[indiceIn:indiceFin]

    # autor
    indiceIn=info.find(pInAutor)
    indiceFin= info.find(pFinAutor)
    autorArt=info[indiceIn:indiceFin]

    # fecha
    indiceIn=info.find(pInFecha)
    indiceFin= info.find(pFinFecha)
    fechaArt=info[indiceIn:indiceFin]

    # articulo
    indiceIn=info.find(pInArt1)
    indiceFin= info.find(pFinArt1)
    articulo=info[indiceIn:indiceFin]

    # 2. LIMPIEZA
    # Limpiar metadatos
    tituloArt = tituloArt[len(pInTit):]
    subTituloArt = subTituloArt[len(pInSubTit):]
    if esPatron2:
        autorArt = autorArt[len(pInAutor):]
    else:
        autorArt = deleteExpresion(autorArt,"<",">")
    fechaArt = fechaArt[len(pInFecha):]

    # Limpiar articulo
    # whiteSpaces y simbolos
    articulo = articulo.replace("\n"," ")
    articulo = deleteExpresion(articulo,"<!--","-->")
    articulo = deleteExpresion(articulo,"<",">")
    #articulo = articulo.replace("—","")
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

    HTMLsAll.append(data)
    titulosAll.append(tituloArt)
    subTitulosAll.append(subTituloArt)
    autoresAll.append(autorArt)
    fechasAll.append(fechaArt)
    articulosAll.append(articulo)

    # Muestro resultados limpios
    print "\n Titulo\n", tituloArt,"\n"
    print "\n SubTitulo\n", subTituloArt,"\n"
    print "\n Autor: ",autorArt,"\n"
    print "\n Fecha: ", fechaArt, "\n"
    #print "\n articulo \n", articulo

    print "\n htmls\n", len(HTMLsAll),"\n"
    print "\n urls\n", len(urlsAll),"\n"
    print "\n tits: ",len(titulosAll),"\n"
    print "\n subs: ", len(subTitulosAll), "\n"
    print "\n autores \n", len(autoresAll)
    print "\n fechas \n", len(fechasAll)
    print "\n articulos \n", len(articulosAll)
    contador +=1
output_table = DataFrame({
                'Htmls' : HTMLsAll,
                'Urls' : urlsAll,
                'Titulos' : titulosAll,
                'SubTitulos' : subTitulosAll,
                'Autores' : autoresAll,
                'Fecha' : fechasAll,
                'Articulos' : articulosAll
                })

#print output_table.get_value(output_table.index[0],'Fecha')

#exportarExcel(output_table)
exportarMatrizCSV(output_table, "NoticiasElTiempo"+str(topePag)+".csv")
#print list(output_table.columns.values)
#print len(output_table.axes[0])
#print len(output_table.axes[1])