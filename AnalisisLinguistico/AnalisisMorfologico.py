#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import prettytable
import string
import ServiciosTecnicos.GestorEntradasSalidas

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

def sumaVectores(lista1, lista2):
    resultado = []
    if lista1<>lista2:
        "ErrorP: No tienen la misma longitud"
        return None
    for i in range(len(lista1)):
        nuevo = lista1[i]+lista2[i]
        resultado.append(nuevo)
    return resultado
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

def getUniqsConFrecuencias(vector):
    # Determina la cantidad de ocurrencias que hay de cada palabra en un vector.
    palabrasUniq = []                                                               # define una lista de palabras sin repeticion
    cantidad = []
    for i in range(len(vector)):
        existe = False
        for j in range(len(palabrasUniq)):
            if vector[i]==palabrasUniq[j]:
                cantidad[j] += 1
                existe=True

                break
        if not existe:
            palabrasUniq.append(vector[i])
            cantidad.append(1)
    return palabrasUniq, cantidad

def getIndicesPalabrasClavesOR(vector, keywords):
    #obtiene los indices donde se encuentran ciertas palabras claves en un vector. El orden de las palabras no es secuencial
    indices= []
    for i in range(len(vector)):
        for j in range(len(keywords)):
            if vector[i]==keywords[j]:
                indices.append(i)
    return indices

def getIndicesPalabrasClavesAND(vector, keywords):
     #obtiene los indices donde se encuentran ciertas palabras claves en un vector. El orden de las palabras es secuencial
    indices= []
    for i in range(len(vector)):
        vector2 = vector[i:i+len(keywords)] # actualiza ventana movil sobre vector, la ventana es del tamaño keywords
        secuencial=True
        for j in range(len(keywords)):
            if vector2[j]<>keywords[j]:
                secuencial=False
                break
        if secuencial==True:
            indices.append(i)
    return indices


def eliminaStopWords(categoriasEliminar, categoriasG, palabras, lemas):
    # dadas ciertas palabras claves, se buscan en el vector de categorias
    # y se eliminan las palabras correspondientes de los vectores de palabras(palabras y lemas)
    # !!!se puede mejorar usando el metodo de obtener indices
    newCat = []
    newLem = []
    newPal = []
    if len(categoriasG)==len(lemas):
        i=0
        j=0
        for i in range(len(lemas)):
            existe= False
            for j in range(len(categoriasEliminar)):
                if categoriasG[i]==categoriasEliminar[j]:
                    existe=True
                    break
            if existe==False:
                    newCat.append(categoriasG[i])
                    newLem.append(lemas[i])
                    newPal.append(palabras[i])
    else:
        print "ERROR: Las categorias y lemas tienen diferente dimension"
    return newPal, newCat, newLem

def frecuenciasRelativasPonderadas(parrafoVector,keywords, pesos, frecuenciasSignificativas=0):
    # Dado un texto y ciertos keywords, retorna un conjunto de palabras cercanas a los keywords, y su cercania relativa.
    # Las palabras se retornan en una matriz de palabras (lista de listas) con la siguiente forma:
    # [[key1,rel1, rel2, rel3 ],
    #   key2,rel1, rel2, rel3 ], ...]
    # las palabras relacionadas a cada keyword seran del segundo termino en adelante.
    #
    # El concepto de cercania busca una solucion semantica sin lograrla, pues no usa contendio lexico, sino que se basa
    # en asignacion de pesos al texto cercano a los keywords (distancia radial), luego cada palabra acumula pesos,
    # los pesos de cada palabra relacionada seran devueltos en una matriz de pesos isomorfa a la de las palabras

    # El tamaño del vencidario (radio de interes) esta dado por el tamaño del vector de pesos, el cual asigna 1 peso en
    # cada casilla que se corresponde con la cercania a cada palabra.
    # Esto es, si L=len(pesos) y k=pos(key) el Vecindario de key es texto[k-L:k+L]

    # NOTA:
    # Considerando el analisis por parrafos, el vecindario sale del parrafo, esto para precisar el contexto semantico.
    # Aun no se implementa la solucion que acepte keywords multiwords

    pivotes = getIndicesPalabrasClavesOR(parrafoVector,keywords)                                                                #capturo los indices de ocurrencias
    palabrasUniq = []                                                                                                   # define una lista de palabras sin repeticion
    cantidad = []
    valor = []
    radio=len(pesos)
    if pivotes==[]:
        print "no hay coincidencias de palabras claves en el texto"
        return
    for pivote in pivotes:
        # recorto para limites del texto
        inicio= pivote-radio if pivote-radio>=0 else 0
        fin = pivote+radio if pivote+radio+1<len(parrafoVector) else len(parrafoVector)-1
        vectorVecindario = parrafoVector[inicio:fin+1] # se pone mas 1 porque recorta en realidad asi [inicio,final)
        pivoteInVector= pivote - inicio
        # recorto para puntos
        #'''
        inicio=0
        fin = len(vectorVecindario)-1
        for i in range(len(vectorVecindario)):

            if vectorVecindario[i] == ".":
                if i<pivoteInVector:
                    inicio = i+1
                if i>pivoteInVector:
                    fin = i-1 # no guaradara el punto en vectorVecindario
                    break
        vectorVecindario = vectorVecindario[inicio:fin+1]
        pivoteInVector= pivoteInVector - inicio # posicion del pivote en el nuevo vectorVecindario
        #'''
        # Alimenta (actualiza) los vectores palabrasUniq, cantidad y valor con un vectorVecindario de palabras.
        for i in range(len(vectorVecindario)):
            existe = False
            posicion = abs(i-pivoteInVector)                                        # determina a cuantas palabras se encuentra i de la palabra clave (pivote)
            for j in range(len(palabrasUniq)):
                if vectorVecindario[i]==palabrasUniq[j]:
                    cantidad[j] += 1
                    if posicion<>0:
                        # la palabra clave (pivote) no suma valor, sin embargo, esta palabra aparecera con valor si ej. violencia (como pivote) esta cerca a violencia (que no es pivote)
                        valor[j] += pesos[posicion-1]
                    existe=True
                    break
            if not existe:
                palabrasUniq.append(vectorVecindario[i])
                cantidad.append(1)
                if posicion<>0: # asi el pivote se agrega pero sin sumar valor
                    valor.append(pesos[posicion-1])
                elif posicion==0:
                    valor.append(0)

    # procesa e imprime el analisis de frecuencias ponderadas
    s= "analisis de frecuencias con :\n " + str(keywords) + "\n"
    print s*40
    matrizOrdenadaValor = ServiciosTecnicos.GestorEntradasSalidas.ordenarTabla([palabrasUniq,cantidad,valor],2) # del gestor de entradas y salidas
    tabla = prettytable.PrettyTable(['Lema', 'Frecuencia', 'Valor'])
    for i in range(len(palabrasUniq)):
        if matrizOrdenadaValor[i][1]>=frecuenciasSignificativas:
            tabla.add_row([matrizOrdenadaValor[i][0], matrizOrdenadaValor[i][1], matrizOrdenadaValor[i][2]])
            #tabla.add_row([palabrasUniq[i], cantidad[i], valor[i]])
    print tabla

def get_vecindario_from_pivote(pivote, texto_palabras, radio, tag_punto):
    # limite izquierdo del vecindario
    limite_izq=0
    pos= limite_izq
    limite_impuesto=False
    for i in range(radio):
        pos = pivote-1-i
        if pos==-1:
            limite_izq=pos+1
            limite_impuesto=True
            break
        elif texto_palabras[pos]==tag_punto:
            limite_izq=pos+1
            limite_impuesto=True
            break
    if not limite_impuesto:
        limite_izq=pos

    #limite derecho del vecindario
    limite_der=len(texto_palabras)-1
    pos=limite_der
    limite_impuesto=False
    for i in range(radio):
        pos = pivote+1+i
        if pos==len(texto_palabras) or texto_palabras[pos]==tag_punto:
            limite_izq=pos-1
            limite_impuesto=True
            break
    if not limite_impuesto:
        limite_der=pos

    # no se guardan los puntos en los vecindarios
    vecindario = texto_palabras[limite_izq:limite_der+1]                                                            # +1 porque recorta asi [inicio,final)
    pivote_vecindario = pivote-limite_izq                                                                           # posicion del pivote en el nuevo vectorVecindario
    return vecindario, pivote_vecindario
def frecuenciasRelativasPonderadas2(texto,keywords_base, pesos, tag_punto = ".",):# frecuenciasSignificativas=0):
    # Dado un texto y ciertos keywords, retorna un conjunto de palabras cercanas a los keywords, y su cercania relativa.
    # Las palabras se retornan en una matriz de keywords (lista de listas) llamdada keywords_all con la siguiente forma:
    # [[key1,rel1, rel2, rel3 ],
    #   key2,rel1, rel2, rel3 ], ...]
    # las palabras relacionadas a cada keyword seran del segundo termino en adelante.
    #
    # El concepto de cercania busca una solucion semantica sin lograrla, pues no usa contendio lexico, sino que se basa
    # en asignacion de pesos al texto cercano a los keywords (distancia radial), luego cada palabra acumula pesos,
    # los pesos acumulados seran devueltos en una matriz de indice de cercania_relativa, isomorfa a keywords_all

    # El tamaño del vencidario (radio de interes) esta dado por el tamaño del vector de pesos, el cual asigna 1 peso en
    # cada casilla que se corresponde con la cercania a cada palabra.
    # Esto es, si L=len(pesos) y k=pos(key) el Vecindario de key es texto[k-L:k+L]
    #
    # NOTA:
    # Considerando el analisis por parrafos, el vecindario no sale del parrafo, esto para precisar el contexto semantico.
    # Aun no se implementa la solucion que acepte keywords multiwords
    texto_palabras = texto.split()
    radio=len(pesos)
    keywords_all =[]

    cercania_relativa_all=[]
    for key in keywords_base:
        keywords_cer = []                                                                                               # son las palabras cercanas a key
        cercania_relativa = []        
        keywords_cer.append(key)
        cercania_relativa.append(0)
        
        # cada pivote es el indice en el texto donde se encuentra una ocurrencia de key, por tanto cada pivote implica un vecindario.
        # -------------------MODIFICAR INDICE PALABRAS CLAVES OR ?????
        # debo limpiar vecindarios duplicados (varios pivotes en el mismo vecindario)?, seguramente es muy poco frecuente...
        pivotes = getIndicesPalabrasClavesOR(texto_palabras,[key])                                                            # capturo los indices de ocurrencias
        if pivotes==[]:
            print "no hay coincidencias de", key,"en el texto"
            continue
        for pivote in pivotes:
            vecindario, pivote_vecindario = get_vecindario_from_pivote(pivote,texto_palabras,radio,tag_punto)
            # Analisis del vecindario.
            # En cada iteracion se analiza 1 palabra, se cuantifica su peso y se actualiza keywords_cer y
            # actualizando palabras relacionadas y sus respectivos pesos
            for i in range(len(vecindario)):
                palabra_analizada = vecindario[i]
                if palabra_analizada==key:
                    continue # asi no podra salir key relacionada a si misma
                existe = False
                distancia_al_pivote = abs(i-pivote_vecindario)
                peso = pesos[distancia_al_pivote-1] #-1 porque el vector comienza en 0
                for j in range(len(keywords_cer)):
                    if palabra_analizada==keywords_cer[j]:
                        #cantidad[j] += 1
                        cercania_relativa[j] += peso
                        existe=True
                        break
                if not existe:
                    keywords_cer.append(palabra_analizada)
                    #cantidad.append(1)
                    cercania_relativa.append(peso)
            #fin analisis vecindario
        keywords_all.append(keywords_cer)
        cercania_relativa_all.append(cercania_relativa)
    for i in range(len(keywords_all)):
        for j in range(len(keywords_all[i])):
            print keywords_all[i][j], cercania_relativa_all[i][j]
        print "otra \n"*10

    '''
    # procesa e imprime el analisis de frecuencias ponderadas
    #s= "analisis de frecuencias con :\n " + str(keywords) + "\n"
    #print s*40
    matrizOrdenadaValor = ServiciosTecnicos.GestorEntradasSalidas.ordenarTabla([palabrasUniq,cantidad,valor],2) # del gestor de entradas y salidas
    tabla = prettytable.PrettyTable(['Lema', 'Frecuencia', 'Valor'])
    for i in range(len(palabrasUniq)):
        if matrizOrdenadaValor[i][1]>=frecuenciasSignificativas:
            tabla.add_row([matrizOrdenadaValor[i][0], matrizOrdenadaValor[i][1], matrizOrdenadaValor[i][2]])
            #tabla.add_row([palabrasUniq[i], cantidad[i], valor[i]])
    print tabla
    '''


def getTodosContextos(textoVector, palabraClaves, signoInicial, signoFinal):
    # Dado un parrafo en formato vector, y una lista de palabras de interes, obtiene el vencindario para cada
    # palabra de interes, dicho vecindario va desde un signo inicial hasta un signo final
    indices = getIndicesPalabrasClavesOR(textoVector, palabraClaves)

    todosContextosPalabraClave =[]
    for i in indices:
        indiceInicial =0
        indiceFinal = len(textoVector)
        j=i
        while i>0:
            if textoVector[i]== signoInicial:
                indiceInicial=i
                break
            i=i-1
        while j<len(textoVector):
            if textoVector[j] == signoFinal:
                indiceFinal=j+1
                break
            j=j+1
        contexto = textoVector[indiceInicial:indiceFinal]
        todosContextosPalabraClave.append(contexto)
    return todosContextosPalabraClave

def getTodosContextosPorNnomios(textoVector, palabraClaves, lemas, signoInicial, signoFinal):
    # Dado un parrafo de categorias gramaticales en formato vector (texto vector), y una lista de n-nomios (palabras claves),
    # obtiene el vencindario de aquellos lemas que cumplan la secuencia de n-nomios, dicho vecindario va desde un signo
    # inicial hasta un signo final

    print "\n N-nomios: " + palabraClaves.__str__()

    indices = getIndicesPalabrasClavesAND(textoVector, palabraClaves)
    todosContextosPalabraClave =[]
    for i in indices:
        indiceInicial =0
        indiceFinal = len(textoVector)
        j=i
        k=i
        while i>0:
            if textoVector[i]== signoInicial:
                indiceInicial=i
                break
            i=i-1
        while j<len(textoVector):
            if textoVector[j] == signoFinal:
                indiceFinal=j+1
                break
            j=j+1

        contexto = lemas[indiceInicial:indiceFinal]
        todosContextosPalabraClave.append(contexto)

        lemasNnomios = lemas[k:k+len(palabraClaves)].__str__()
        print "\n\n otro N-nomio \n",lemasNnomios, "\n", contexto
    return todosContextosPalabraClave

def palabrasXlemas(buscado, lemas, palabras):
    pal = []
    for i in range(len(lemas)):
        if buscado==lemas[i]:
            pal.append(palabras[i])
    uniq, cantidad= getUniqsConFrecuencias(pal)
    matrizOrdenada = ServiciosTecnicos.GestorEntradasSalidas.ordenarTabla([uniq,cantidad],1)
    for i in range(len(uniq)):
        print matrizOrdenada[i][0], matrizOrdenada[i][1] # no pude mostrarlo en la tabla, error inexplicable

def vector2paragraph(vector, separador=" "):
    return separador.join(vector)

def modificarTaggedTNT(terminosAgregar, categoriasAgregar, lemasAgregar, terminos, categorias, lemas):
    # agrega categorias y lemas personalizados a una lista de los mismos previamente definida,
    # los terminos no son retornados puesto que estos no cambian

    for j in range(len(terminosAgregar)):
        indices = getIndicesPalabrasClavesOR(terminos,[terminosAgregar[j]])
        for i in indices:
            categorias[i]= categoriasAgregar[j]
            lemas[i]=lemasAgregar[j]
    return categorias, lemas

def deleteDuplicateString(sentence):
    return " ".join(sentence.split())