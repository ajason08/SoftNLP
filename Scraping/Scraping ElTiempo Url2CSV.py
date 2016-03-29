#!/usr/bin/python
# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
from pandas import *
import re
from urllib import *
import sys
from ServiciosTecnicos.GestorEntradasSalidas import *
#from AnalisisLinguistico.AnalisisMorfologico import *
import time
import numpy
'''
ini = timeit.timeit()
fin = timeit.timeit()
print abs((fin-ini)*1000)
'''

'''
ESTE SCRIPT OBTENDRÁ TODAS LOS ARTICULOS DE UNA PAGINA WEB DE PERIODICOS LA CUAL CUMPLA CON PATRONES DE SCRAPING,

---VERSION - EL TIEMPO
Se deeben tener en cuenta las siguientes consideraciones:
La pagina del tiempo parece vigilar los accesos, cancelando el ingreso de la ip cuando son demasiado frecuente
'''


def getOcurrenciasExpresion(texto, patronInicio, patronFin):
    # retorna una lista con las ocurrencias del patron
    expresion = patronInicio+".*?"+patronFin
    listaE =re.findall(expresion,texto)
    return listaE

def getUniqs(vector):
    uniqs =[]
    for elemento in vector:
        existe = False
        for uniq in uniqs:
            if elemento==uniq:
                existe=True
                break
        if not existe:
            uniqs.append(elemento)
    return uniqs
def getOcurrenciasExpresiones(texto,expresiones):
    # retorna la lista con las ocurrencias de los patrones
    listaE = []
    for expresion in expresiones:
        listaE = listaE +re.findall(expresion,texto)
    return listaE
def getHtmlFromUrl(indice):
    print "Leyendo pagina", indice,"..."
    url = myUrl+indice.__str__()+"&orden=reciente"
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
        todasPagUrls.append(indice)

#'''# NIVEL LISTAS: OBTENER TODAS LAS URL DE LAS NOTICIAS
topeInicio=5002
topeFin=6001

fallidasOutput = (np.ones(topeFin-topeInicio)).astype(int)
urlsAll = []
todasPagUrls = []
urlsCorruptas = [] # aqui patrones detectados para saltarse url
fails = []
log = []
miUrl = ""

patronInicio= "                <time"
patronInicio2="href=\"http:"
patronFin2='">'
myUrl = "http://www.eltiempo.com/archivo/buscar?q=+&producto=eltiempo&seccion=4&pagina="

print "Se procesaran", topeFin-topeInicio, "paginas..."
for i in range(topeInicio,topeFin+1):
    try:
        getHtmlFromUrl(i)
    except:
        print "elf", sys.exc_info()[0]
        #registra fallos
        fails.append(i)
        logT = "reintento", miUrl
        log.append(logT)
        print logT
        # reintenta
        time.sleep(5)
        indice=i-1
print "fails a reintentar por ultima vez", len(fails), fails
exit()
for i in range(len(fails)):
    try:
        getHtmlFromUrl(fails[i])
        # si es exitoso saquelo de los fails---- sin probar
        del(fails[i])
        i=i-1
    except:
        print "reintento final fallido en"
        if fails[i] <> None:
            print "::", fails[i]
print "fails reincidentes", len(fails), fails
for fail in fails:
    fallidasOutput[fail]=0

print "p1", len(fallidasOutput), len(urlsAll)
output_table = DataFrame({
        'Urls' : urlsAll,
        'fallidas': fallidasOutput
        })
#exportarMatrizCSV(output_table, "UrlsElTiempoBogotaxprueba.csv")
#output_table2 = DataFrame({
#        'LOG' : log
#        })
#exportarMatrizCSV(output_table2, "logBogotaxprueba.csv")


