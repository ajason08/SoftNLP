#!/usr/bin/python
# -*- coding: utf-8 -*-
from AnalisisLinguistico.AnalisisMorfologico import *
from ServiciosTecnicos.GestorEntradasSalidas import *

def obtenerEntidadesFuerzaBruta(texto, entidadesConocidas):
    # identifica las entidades en un texto* (texto es un vector de textos) basandose en
    # una lista de entidades conocidas. comprueba en cada palabra si corresponde a una entidad.

    # limitaciones:
    # no reconoce el nombre completo cuando presenta una abreviatura en medio

    contadorArt=0
    nombresPorArticulo = []
    for articulo in texto:
        nombresArticuloX = []

        palabras = articulo.split()

        nombreCompleto=False
        constructorNombre= ""
        nroNombresCostruc = 0
        nroPalabra=1
        for palabra in palabras:
            #evita no reconocer una entidad por tener puntuacion
            if palabra.__contains__("."):
                palabra = palabra.replace(".","")
                nombreCompleto=True
            if palabra.__contains__(","):
                palabra = palabra.replace(",","")
                nombreCompleto=True

            # La entidad continua hasta que se encuentra con una noEntidad
            esNombre=False
            for nombre in entidadesConocidas:
                if palabra == nombre:
                    esNombre =True
                    constructorNombre = constructorNombre+" "+palabra
                    nroNombresCostruc = nroNombresCostruc+1
                    break
            if not esNombre:
                nombreCompleto=True
            if nombreCompleto:
                if nroNombresCostruc <> 0:
                    if nroNombresCostruc > 1:       #filtra por un nro minimo de entidades contiguas
                        nombresArticuloX.append(constructorNombre)
                        nombresArticuloX.append(nroPalabra)
                    constructorNombre = ""
                    nroNombresCostruc=0
                nombreCompleto=False
            nroPalabra= nroPalabra+1
        nombresPorArticulo.append(nombresArticuloX)
        contadorArt =contadorArt+1
        if contadorArt ==5:
            break
    cont =1
    for nombreArtX in nombresPorArticulo:
        print texto[cont-1]
        print cont, nombreArtX, "\n"*2, "lol"
        cont = cont+1

def getEntidadesMayus(texto, entidadesConocidas, nroMinPalabrasEnEntidad=0, nroMaxEntidad=100):
    # identifica las entidades en un texto* (texto es un vector de textos) basandose en una lista de entidades conocidas.
    # Entidad: el principio mayus es aquel que define una Entidad como aquel grupo de palabras cuya palaba inicial
    # se encuentra presente en la lista de entidadesConocidas y las demas comienza con mayuscula o son entidadesConectoras.
    #  Ej. Maria de la Rosa, Juan C Diaz, Juan C. Diaz, Armando de Mesa.
    # No son entidades aquellos grupos de palabras que no cierren conexion. Ej. Maria de la, Armando de mesa

    # Entrada:
    # texto: contiene el conjunto de textos a analizar, debe ser un vector.
    # entidadesConocidas: Lista de entidades conocidas
    # nroMinimoPalabrasEnEntidad: Es el numero minimo de palabras que debe tener una entidad Ej. Maria de la rosa tiene 4

    # Salida:
    # textosMarcado: es un vector con los textos de entrada pero con las marcas que resaltan las entidades
    # entidadesPorTexto: es un vector con la lista de entidades encontradas en cada texto
    marcaNegritaI = "<b>"
    marcaNegritaF = "</b>"
    marcaEntidad  = "#"

    conectoresEntidad = "de,del,los,la,las".split(",")
    puntacionSeparadora = ".#,#;".split("#")

    contadorArt=0
    nombresPorArticulo = []
    textosMarcados = []


    for articulo in texto:
        textosMarcados.append("")
        nombresArticuloX = []
        palabras = articulo.split()

        constructorEntidad= ""
        nroPalabrasEntidad = 0
        estoyEnUnNombre = False
        esperandoCierreConexion=False
        palabraConectora=False
        for palabra in palabras:
            #evita no reconocer una entidad por tener puntuacion
            palabraPuntuada=False
            puntuacionSalvada= ""
            for puntuacion in puntacionSeparadora:
                if palabra.__contains__(puntuacion):
                    #la abreviatura de nombre suele ser la inicial y el punto. Ej. Juan C. Restrepo
                    if len(palabra)>2:
                        palabra = palabra.replace(puntuacion,"")
                        palabraPuntuada=True
                        puntuacionSalvada= puntuacion+" "
                    break
            #evita no reconocer una entidad por estar toda en mayuscula o mal escrita en sus mayusculas
            if len(palabra)>1 and palabra[1].isupper():
                palabra = palabra.capitalize()

            #Busqueda de la proxima entidad, la cual comienza una palabra presente en la lista de entidades
            if not estoyEnUnNombre:
                for nombre in entidadesConocidas:
                    #palabra = str(palabra)
                    if palabra == nombre:
                        estoyEnUnNombre=True
                        break
            # La entidad se construye mientras estoy en un nombre
            if estoyEnUnNombre:
                # Controlo cierre de conexion
                if palabraConectora and not conectoresEntidad.__contains__(palabra) and palabra[0].isupper():
                    # la palabra anterior era conectora pero esta ya no lo es y comienza con mayus
                    esperandoCierreConexion=False
                palabraConectora =conectoresEntidad.__contains__(palabra)
                if palabraConectora:
                    esperandoCierreConexion=True

                if palabra[0].isupper() or palabraConectora:
                    constructorEntidad = constructorEntidad+" "+palabra
                    nroPalabrasEntidad = nroPalabrasEntidad+1
                entidadFinalizada = palabraPuntuada or (not palabra[0].isupper() and not palabraConectora)
                if entidadFinalizada:
                    estoyEnUnNombre = False
                    if nroPalabrasEntidad <> 0:    # filtrado: si no tiene entidades no agregue # SE PUEDE QUITAR ESTA LINEA?
                        # filtrado: si nro minimo de entidades contiguas, y finalizo conexxion --> Agrega entidad
                        if nroMinPalabrasEnEntidad < nroPalabrasEntidad and nroPalabrasEntidad < nroMaxEntidad and not esperandoCierreConexion:
                            nombresArticuloX.append(constructorEntidad)
                            entidad = marcaNegritaI+constructorEntidad+" "+marcaNegritaF
                            textosMarcados[contadorArt] += entidad+" "
                        else:#sin marcas, no es entidad
                            textosMarcados[contadorArt] += constructorEntidad+" "
                        # la ultima palabra (la actual) pudo no haberse tenido en cuenta para la construccionEntidad
                        if not constructorEntidad.__contains__(palabra):
                            textosMarcados[contadorArt] += palabra+" "
                        constructorEntidad = ""
                        nroPalabrasEntidad=0
                    esperandoCierreConexion=False

            else:#Agregar palabra normal al textoMarcado
                textosMarcados[contadorArt] += palabra+" "
            textosMarcados[contadorArt] += puntuacionSalvada
        nombresPorArticulo.append(nombresArticuloX)
        contadorArt =contadorArt+1


        if contadorArt ==4:                 # para que lea solo los primeros n articulos
            break

    entidadesPorTexto = []
    #Muestro los resultados.
    for cont in range(len(nombresPorArticulo)):
        #print cont+1, "\n"
        #print texto[cont]
        #print "\n"*2, "CON MARCAS", "\n"*2, textosMarcados[cont], "\n"
        nombresArtX = nombresPorArticulo[cont]
        entidadesPorTexto.append(marcaEntidad.join(nombresArtX))
        #print marcaEntidad.join(nombresArtX)
    return textosMarcados, entidadesPorTexto

def getEntidadesSinFalsosPositivos(textoMarcado, entidadesResueltas, entidadesSospechosas, porcentajeDeteccion):
# Este metodo se usa para pulir un poco resultados del metodo getEntidadesMayus.
# Si una entidadX se compone en mas de un "porcentajeDeteccion"% la entidad será marcada como falsoPositivo

# ENTRADA:
    # entidadesResueltas: es el vector de entidades devuelvo por el metodo getEntidadesMayus.
    # entidadesSospechosas: es una lista de entidades que suelen ser causa de falsos positivos. Ej. Juez, Rios, etc.
        # esta lista deberia incluir tambien terminos los cuales se sabe que no son entidades de nuestro dominio.
        # Para obtenerlas, un metodo es crear una lista sin repeticion de todas las subentidades de getEntidadesMayus
        # (Pedro, Juez, Circuito, Bogotá etc) y restarle entidadesConocidas.
        # Notese ademas que esta lista resultante puede ser usada para aumentar entidadesConocidas
    # PorcentajeDeteccion: % de palabras sospechosas en una entidad para ser considerada falso positivo. Ej: 0.5
# SALIDA:
    # entidadesSinFalsosPositivos

# NOTA
# Al contrario de lo que pueda pensarse, respecto a getEntidadesFuerzaBruta, getEntidadesMayus+getEntidadesSinFalsosPositivos
# tiene mayor eficiencia (pues no rreccore todas entidaesConocidas y no evalua cada entidadX en el pulimiento) y
# eficacia (pues reconoce conectores y por su criterio mayus permite detectar entidades faltantes en la BD conocidas)



    conectoresEntidad = "de,del,los,la,las".split(",")
    entidadesSinFalsosPositivos = []
    listFalsosPositivos = []

    textoMarcadoSinFP=[]
    marcaNegritaI = " <b>"
    marcaNegritaF = " </b>"

    cont = 0
    # entidadesResueltas tiene la forma: [entidad1#entidad2#entidad3,  entidad4#entidad5#entidad6...]
    for entidadesX in entidadesResueltas:
        # en cada iteracion crea una entidadesXListSinFP que sera fila de entidadesSinFalsosPositivos
        # entonces len(entidadesResueltas)==len(entidadesSinFalsosPositivos)== len(listFalsosPositivos). Siempre
        entidadesXListSinFP = []
        falsosPositivosX = []

        # entidadesXList tiene la forma: [Juan Manuel Garcia, Segundo Penal Especializado, Pedro Paramo]
        entidadesXList = entidadesX.split("#")
        for entidadX in entidadesXList:
            # entidadX tiene la forma: Juan Manuel Garcia
            entidadXList = entidadX.split()
            sospechosasDetectadas = 0
            nroEntidades = len(entidadXList)
            falsoPositivo = False
            print "NUEVA ENTIDAD"
            # entidadXList tiene la forma: [Juan, Manuel, Garcia]
            for subEntidad in entidadXList:
                if conectoresEntidad.__contains__(subEntidad):
                    nroEntidades-=1
                    continue
                if entidadesSospechosas.__contains__(subEntidad):
                    sospechosasDetectadas+=1
                    nivelSospecha = sospechosasDetectadas*1.0/nroEntidades
                    print "   ----ENTIDAD SOSPECHOSA", subEntidad, "NivelSospecha", nivelSospecha
                nivelSospecha = sospechosasDetectadas*1.0/nroEntidades
                if nivelSospecha>=porcentajeDeteccion:
                    falsoPositivo=True
                    falsosPositivosX.append(entidadX)
                    print "DECLARADA Falso positivo: ", entidadX
                    break
            if not falsoPositivo:
                print "DECLARADA valido: ", entidadX
                entidadesXListSinFP.append(entidadX)
                # se espera que contenga al final: [Juan Manuel Garcia, Pedro Paramo]
        entidadesSinFalsosPositivos.append(vector2paragraphSeparador(entidadesXListSinFP, "#"))
        listFalsosPositivos.append(vector2paragraphSeparador(falsosPositivosX, "#"))

        # Actualizo el textoMarcado para que no tenga FP
        txtmSinFP = textoMarcado[cont]
        # para el replace, los espacios en marcaNegrita deben ser consistentes con los que se tienen en texto marcado y fp
        for fp in falsosPositivosX:
            fpm=marcaNegritaI+fp+marcaNegritaF
            txtmSinFP = txtmSinFP.replace(fpm,fp)
        cont +=1
        textoMarcadoSinFP.append(txtmSinFP)

    #muestro resultados
    cont =0
    print "-----Resultados"
    for cont in range(len(textoMarcado)):
        print "\n"*2,cont,"falsos positivos en texto: ", listFalsosPositivos[cont]
        print "\n",textoMarcado[cont],"\n"*2,textoMarcadoSinFP[cont]

    return textoMarcadoSinFP, entidadesSinFalsosPositivos


#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -Main- - - - - - - - - - - - - - - - - - - - - - - - - - -

archivoNombres = "Names.xls"
archivoNoticias = "39Art.txt"
archivoNoEntidades = "FalsosPositivos.xls"
sospechosas = "FalsosPositivos.xls"

nombres=   cargarColumnaEnLista(archivoNombres,0,0,1,3500)
apellidos= cargarColumnaEnLista(archivoNombres,1,0,1,3500)
listaNombresApellidos =nombres+apellidos

noticias = cargarcsv(archivoNoticias, "#")

#print listaNombresApellidos

#obtenerEntidadesFuerzaBruta(noticias,listaNombresApellidos)
textoMarcado, entidadesResueltas = getEntidadesMayus(noticias,listaNombresApellidos,1)
#print entidadesResueltas

noEntidades = cargarColumnaEnLista(archivoNoEntidades,0,0)
sospechosas = cargarColumnaEnLista(sospechosas,0,0)
sospechosas = sospechosas+noEntidades
getEntidadesSinFalsosPositivos(textoMarcado, entidadesResueltas,sospechosas,0.5)



#problemas con la base de datos de nombres
    # contiene cosas que no son nombres o apellidos: "Gastos varios"
    # La seccion de apellidos tiene nombres y apellidos en una misma linea
    # añadir nombres con tildes. josé no lo reconoce
    # Mejora por identificacion de causantes falsos positivos
        # se puede tener una base de entidades con alta probabilidad de no ser apellidos o nombres,
        # ej, Juez, Distrito, Medio, Florida. Si una entidad compuesta presenta muchoss de estos se descarta
#problemas con la base de datos de noticias
    # luego de una coma no ponene espacio luego, en Vaupés,Fabio Arango Torres, solo reconoce, Arango Torres
    # todas las palabras conectoras deben ser pasadas a minuscula. o agregar variantes con mayus a lista conectoras.
#Problemas sin solución
# reconoce entidades que no son nombres o apellidos.


#Hallazgos:
# los nombres aislados son utiles para encontrar palabras que no estan en la BD de nombres u otra tipo de entidades.
# Los alias son facilmente encontrados por las comillas.




