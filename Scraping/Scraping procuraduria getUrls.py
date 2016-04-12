#!/usr/bin/python
# -*- coding: utf-8 -*-

from pandas import *
import re
from urllib import *
import sys
#from ServiciosTecnicos.GestorEntradasSalidas import *
import time
import numpy
'''
ini = timeit.timeit()
fin = timeit.timeit()
print abs((fin-ini)*1000)
'''

'''
ESTE SCRIPT OBTENDRÁ TODAS LAS URL DE NOTICIAS EN UNA PAGINA WEB QUE CUMPLA CON PATRONES DE SCRAPING,

---VERSION - procuraduria
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
    url = myUrl+indice.__str__()
    print "listado", url
    usock = urlopen(url)
    data = usock.read()
    data = data.decode("latin-1")
    usock.close()

    #recorto la seccion donde estan las url
    init = data.index(patronInicio)
    fin = data.index(patronFin)
    data = data[init:fin]

    listaE= getOcurrenciasExpresion(data,patronInicio2,patronFin2)
    #obtengo urls limpias
    #listaE =getUniqs(listaE)
    for url in listaE:
        inapropiado = getOcurrenciasExpresiones(url,urlsCorruptas)
        if inapropiado <> []:
            print "--DESCARTADO-- Se encontro:", inapropiado
            continue
        url = url[len(patronInicio2):len(patronFin2)*-1]
        url= "http://www.procuraduria.gov.co/portal/"+url
        urlsAll.append(url)
        todasPagUrls.append(indice)

#'''# NIVEL LISTAS: OBTENER TODAS LAS URL DE LAS NOTICIAS


#parametros
categoria = 3
# paginas contiene los sufijo que determinan la pagina dentro de una categoria, cada pagina contiene 10 links a noticias
paginas = range(0,10,10)#270

fallidasOutput = (np.ones(len(paginas))).astype(int)
urlsAll = []
todasPagUrls = []
urlsCorruptas = [] # aqui patrones detectados para saltarse url corrupta
fails = []
log = []
miUrl = ""


urlBase = "http://www.procuraduria.gov.co/portal/index.jsp?option=net.comtor.cms.frontend.component.pagefactory.NewsComponentPageFactory&action=view-category&category="
sufijoUrl = '&wpgn=null&max_results=10&first_result='
myUrl=urlBase+categoria.__str__()+sufijoUrl

#detecta la zona donde estan las urls
patronInicio= '<p>Actualidad y noticias</p>'
patronFin='siguiente noticia</p><br>'
#detecta la url por lo que tiene al rededor
patronInicio2= 'href="'
patronFin2='" class='

print "Se procesaran", len(paginas), "paginas..."
for pagina in paginas:
    getHtmlFromUrl(pagina)

# Salida
for url in urlsAll:
    print url

output_table = DataFrame({
        'Urls' : urlsAll
        })



# reintentar fallas
'''
print "fails a reintentar por ultima vez", len(fails), fails

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


exportarMatrizCSV(output_table, "UrlsElTiempoBogotaxprueba.csv")
output_table2 = DataFrame({
       'LOG' : log
        })
exportarMatrizCSV(output_table2, "logBogotaxprueba.csv")
'''
