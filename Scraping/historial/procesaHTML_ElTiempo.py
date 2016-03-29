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
topeInicio=297
topePag= 0
print "Se procesarán", topePag, "páginas..."
urlsAll = []
todasPagUrls = []
urlsCorruptas = ["ecbloguer"] # ecbloguer es un blog externo de elcolombiano.com


patronInicio= "                <time"
patronInicio2="href=\"http:"
patronFin2='"'

for i in range(topeInicio,topeInicio+topePag+1):
    print "Leyendo página", i,"..."
    url = "http://www.eltiempo.com/archivo/buscar?q=+&producto=eltiempo&seccion=25&pagina="+i.__str__()
    print "listado", url
    usock = urlopen(url)
    data = usock.read()
    data = data.decode("utf-8")
    usock.close()
    #recorto la seccion donde estan las url
    init = data.index(patronInicio)
    data = data[init:init+10000]

    listaE= getOcurrenciasExpresion(data,patronInicio2,patronFin2)
    #obtengo urls limpias
    listaE =getUniqs(listaE)
    for url in listaE:
        inapropiado = getOcurrenciasExpresiones(url,urlsCorruptas)
        if inapropiado <> [] :

            print "--DESCARTADO-- Se encontro:", inapropiado
            continue
        url = url[len(patronInicio2):len(patronFin2)*-1]
        url= "http:"+url
        urlsAll.append(url)
        todasPagUrls.append(i)
        #print url, "\n"*2






#exit()


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


j=1
cantidadArt=0
contador=0
while contador < len(urlsAll):
    url = urlsAll[contador]
    print "-------- ARTICULO NUEVO ----------", j, "pagina", todasPagUrls[j-1]
    print url
    j=j+1

    # HTML completo
    usock = urlopen(url)
    data = usock.read()
#    data = data.decode("utf-8") se usa en knime
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
        pInInf = '<h2 itemprop="name">'
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
    articulo = articulo.replace("—","")
    articulo = articulo.replace("#","")
    #comillas
    articulo = articulo.replace("”"," ' ")
    articulo = articulo.replace("“"," ' ")
    articulo = articulo.replace("‘"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace("’"," ' ")
    articulo = articulo.replace('"'," ' ")
    # codificacion html
    articulo = articulo.replace("&aacute;","á")
    articulo = articulo.replace("&eacute;","é")
    articulo = articulo.replace("&iacute;","í")
    articulo = articulo.replace("&oacute;","ó")
    articulo = articulo.replace("&uacute;","ú")
    articulo = articulo.replace("&ntilde;","ñ")
    articulo = articulo.replace("&uuml;","ü")
    articulo = articulo.replace("&Aacute;","Á")
    articulo = articulo.replace("&Eacute;","É")
    articulo = articulo.replace("&Iacute;","Í")
    articulo = articulo.replace("&Oacute;","Ó")
    articulo = articulo.replace("&Uacute;","Ú")
    articulo = articulo.replace("&Ntilde;","Ñ")
    articulo = articulo.replace("&Uuml;","Ü")
    articulo = articulo.replace("&iquest;","¿")
    articulo = articulo.replace("&nbsp;"," ")
    articulo = articulo.replace("&ldquo;"," ' ")
    articulo = articulo.replace("&rdquo;"," ' ")
    articulo = articulo.replace("&lsquo;"," ' ")
    articulo = articulo.replace("&rsquo;"," ' ")
    articulo = articulo.replace("&iexcl;"," ¡ ")
    articulo = articulo.replace("&deg;"," ° ")
    articulo = articulo.replace("&ndash;"," - ")
    articulo = articulo.replace("&ordf;"," ")
    # casos especiales
    articulo = articulo.replace(chr(9),"")      # tabulador normal
    articulo = articulo.replace(chr(10),"")     # tabulador extraño
    articulo = articulo.replace(chr(13),"")     # tabulador extraño 2
    # final
    articulo = articulo.strip()


    # 2.1 cortar si encontro codigo en medio del patron, fue codificado por precausion, nunca lo he usado.
    articuloVector = str(articulo).split()
    indiceTerminosInapropiados = getIndicesPalabrasClavesOR(articuloVector,terminosInapropiados)
    if indiceTerminosInapropiados <> []:
        print "--RECORTADO-- En este articulo encontro uno de los sgts terminos inapropiados", indiceTerminosInapropiados
        #print "--Articulovector antes--", articuloVector
        print "--Articulovector antes--",len(articuloVector)
        articuloVector = articuloVector[0:min(indiceTerminosInapropiados)]
        print "--Articulovector despues--",len(articuloVector)
        #print "--Articulovector despues--", articuloVector
        #probar meterlo dentro del if
        articulo = vector2paragraph(articuloVector)



    # Muestro resultados limpios
    print "\n Titulo\n", tituloArt,"\n"
    print "\n SubTitulo\n", subTituloArt,"\n"
    print "\n Autor: ",autorArt,"\n"
    print "\n Fecha: ", fechaArt, "\n"
    print "\n articulo \n", articulo
    contador +=1

    # 3. ALMACENAR EL ARTICULO
    outputArt.write(articulo+" # ")
    if cantidadArt <>0: #primera iteracion
        outputUrl.write(",")
    outputUrl.write(url)
    cantidadArt+=1
outputArt.close()
outputUrl.close()
print "\nRESULTADO: ",cantidadArt, "articulos salvados en","'"+nombreArchivo+"'", "\nLas urls las puedes encontrar en","'"+nombreArchivoUrls+"'"
# FIN  NIVEL ARTICULO



