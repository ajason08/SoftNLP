#!/usr/bin/python
# -*- coding: utf-8 -*-
from AnalisisLinguistico.AnalisisMorfologico import *
from ServiciosTecnicos.GestorEntradasSalidas import *
def getArticulos(vector, bandera):
    # intentarlo con split
    keyword =[bandera]
    indices = getIndicesPalabrasClavesOR(vector, keyword)
    inicial=0
    articulos=[]
    for i in indices:
        articulo = vector[inicial:i]
        articulos.append(articulo)
        inicial = i+1
    return articulos

def maximo(lista):
    posMax=0
    for i in range(1,len(lista)):
        if lista[i]>lista[posMax]:
            posMax=i
    if(lista[posMax]<2):
        posMax = -1
    return posMax


'''
# cargo palabras, categorias y lemas sin stopwords
cantidadPaginas = 5
archivoTxt =str(cantidadPaginas)+'Tag.txt'
palabrasN, categoriasN, lemasN = cargarArchivoTaggerTNT(archivoTxt)
#Quito terminos irrelevantes para este analisis
archivoExcel = "analisis.xls"
stopWords= cargarColumnaEnLista(archivoExcel,0,5,1,0)
newPal, newCat, newLem = eliminaStopWords(stopWords,categoriasN, palabrasN, lemasN)
#Agreggo terminos relevantes para este analisis
palabrasA= cargarColumnaEnLista(archivoExcel,0,7,1,0)
categoriaA=cargarColumnaEnLista(archivoExcel,0,8,1,0)
lemaA = cargarColumnaEnLista(archivoExcel,0,9,1,0)
# agrego constantes manuales
newCat, newLem = modificarTaggedTNT(palabrasA,categoriaA,lemaA,newPal,newCat,newLem)
'''

# VER UNKNOWNS
#palabrasXlemas("<unknown>", newLem, newPal)
miTexto = codecs.open("xART.txt", "r",encoding='utf-8').read()
keywords = ["ministro","fiscalia"]
 # obtener keywords relacionados
pesos = range(1,10)
pesos.reverse()
#print "PESOS", pesos, len(pesos), exit()
frecuenciasRelativasPonderadas2(miTexto, keywords, pesos)
exit()


# CLASIFICACION

articulos = getArticulos(newLem,"#")

articulosNormales =getArticulos(palabrasN,"#")
urls = cargarcsv(str(cantidadPaginas)+"Url.txt",",")
#print urls
#for uin urls:
    #print "url:",u,"\n"
keywords = ["violencia"]

''' IMPRIMIR CONTEXTOS COMPLETOS
# estos contextos seran utiles para determinar las expresiones comunes (palabras y colocaciones) para cada tipo de violencia

# analisis de n-nomios
nnomio = ["ART", "NC", "PDEL"]
#contextosGramat=  getTodosContextosPorNnomios(categoriasG, nnomio, lemas, "FS","FS")

# analisis por palabra clave
articulosEnContextos = [] # contendra una lista de articulos, cada uno formado por un conjunto de contextos (vecindarios)
for articulo in articulos:
    articulosEnContextos.append(getTodosContextos(articulo,keywords, ".", "."))
contArt=1
for articulo in articulosEnContextos:
    contContx=1
    print "\n"*2
    print "Este es el articulo #", contArt, articulo, "\n"
    for y in articulo:
        z= vector2paragraph(y)
        print "y este es su contexto #",contContx,"\n", z
        contContx+=1
    contArt+=1

#Probar expresiones
archivoExcel = "clasificacionExpresiones.xls"
expresionesConflictoInterno =  cargarColumnaEnLista(archivoExcel,0,0,1,0)
pruebaLema=vector2paragraph(newLem)
categ, cant =getUniqsConFrecuencias(getOcurrenciasExpresiones(pruebaLema,expresionesConflictoInterno))
for i in range(len(categ)):
    print categ[i], cant[i]
'''


archivoExcel = "clasificacionExpresiones.xls"
expresionesConflictoInterno =  cargarColumnaEnLista(archivoExcel,0,0,1,0)
expresionesMetropolitana = cargarColumnaEnLista(archivoExcel,0,1,1,0)
ExpresionesViolenciaRural = cargarColumnaEnLista(archivoExcel,0,2,1,0)
ExpresionesViolenciaNarcotrafico = cargarColumnaEnLista(archivoExcel,0,3,1,0)
ExpresionesViolenciaMujer = cargarColumnaEnLista(archivoExcel,0,4,1,0)
ExpresionesViolenciaAnimales = cargarColumnaEnLista(archivoExcel,0,5,1,0)

clasificacion=[]
clasNada=[]
clasMetro= []
clasConf = []
clasnarco = []
clasrural = []
clasmujer = []
clasanimal = []

for articulo in articulos:
    articulo= vector2paragraph(articulo)
    ocurrConfInt= len(getOcurrenciasExpresiones(articulo,expresionesConflictoInterno))
    ocurrMetro  = len(getOcurrenciasExpresiones(articulo,expresionesMetropolitana))
    ocurrRural  = len(getOcurrenciasExpresiones(articulo,ExpresionesViolenciaRural))
    ocurrNarco  = len(getOcurrenciasExpresiones(articulo,ExpresionesViolenciaNarcotrafico))
    ocurrMujer  = len(getOcurrenciasExpresiones(articulo,ExpresionesViolenciaMujer))
    ocurrAnimal = len(getOcurrenciasExpresiones(articulo,ExpresionesViolenciaAnimales))
    lista =[ocurrConfInt,ocurrMetro, ocurrRural,ocurrNarco,ocurrMujer,ocurrAnimal]
    max = maximo(lista)
    if max == 0:
        clasificacion.append("Violencia por conflicto interno")
        clasConf.append(articulo)
    elif max == 1:
        clasificacion.append("Violencia en el area metropolitana")
        clasMetro.append(articulo)
    elif max == 2:
        clasificacion.append("Violencia en zonas rurales")
        clasrural.append(articulo)
    elif max == 3:
        clasificacion.append("Violencia por narcotrafico")
        clasnarco.append(articulo)
    elif max == 4:
        clasificacion.append("Violencia contra la mujer")
        clasmujer.append(articulo)
    elif max == 5:
        clasificacion.append("Violencia por maltrato animal")
        clasanimal.append(articulo)
    else:
        clasificacion.append("Ningun tipo de violencia en particular")
        clasNada.append(articulo)
categorias, cantidad = getUniqsConFrecuencias(clasificacion)

print "----- RESULTADOS DE CLASIFICACION -----"
for i in range(len(categorias)):
    print categorias[i], cantidad[i]

print len(urls),"-", len(clasificacion)
exportarExcelClasificacion(urls,clasificacion)


print "las de nada-----------------------------------------------------------"
for n in clasNada:
    print "nuevo art"
#    print vector2paragraph(n), "\n"
    print n, "\n"


# HACER MEJORAS:
# determinar que articulos no son de violencia a pesar incluyan la palabra
# determinar si el algoritmo encuentra los articulos de violencia dentrod e una lista de articulos x