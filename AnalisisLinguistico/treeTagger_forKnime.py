from pandas import *
import codecs
import os
import re
import subprocess
def printVector(vector):
    for x in vector:
        print x

def vector2paragraph(vector, separador=" "):
    return separador.join(vector)

def callTreeTagger(fileIn, dirIO, dirActual):
    os.chdir(dirIO)
    comandoTT='tag-spanish ' +fileIn
    proc = subprocess.check_output(comandoTT, shell=True)
    os.chdir(dirActual)
    return proc

def ocurrenciasPalabra(texto, palabra_buscada):
    # cuenta el numero de veces que una palabra aparece en un texto
    nroOcurrencias=0
    for palabra in texto.split():
        if palabra==palabra_buscada:
            nroOcurrencias+=1
    return nroOcurrencias
def ocurrenciasinVector(vector, elemento):
    # cuenta el numero de veces que una palabra aparece en un texto
    nroOcurrencias=0
    for e in vector:
        if e==elemento:
            nroOcurrencias+=1
    return nroOcurrencias

def estructurarTagged(outString,output=0):
    formas=[]
    tags=[]
    lemas=[]
    #print outString.decode("utf-8")
    for tagged_word in outString.split("\n"):
        tagged_word_vector = tagged_word.split()
        if len(tagged_word_vector)==0:
            continue                
        #la forma es compuesta como en "por que" o "a traves de"
        formaCompuesta =vector2paragraph(tagged_word_vector[0:-2],"_")            
        formas.append(formaCompuesta)
        tags.append(tagged_word_vector[-2])
        lemas.append(tagged_word_vector[-1])
    if output:
        for i in range(len(lemas)):
            print formas[i].decode("utf-8"), lemas[i].decode("utf-8"), tags[i].decode("utf-8")
    '''
    #asegurar que el texto termine en punto
    if lemas[-1]<>".":
        formas.append(".")
        lemas.append(".")
        tags.append("Fp")
        probs.append("1")
    '''
    return formas, lemas, tags

# directorios a usar
dirTreeTagger = 'C:\Perl64\\bin'
dirEntradaSalida = dirTreeTagger
dirActual = os.getcwd()

# estructuras de salida
formasFinal= []
lemasFinal= []
tagsFinal= []

entrada = "input.txt"
# tabla de entrada en knime
for art in input_table['Articulos']:    
    # creo entrada para tagger en dir especifico
    os.chdir(dirEntradaSalida)
    file = codecs.open(entrada, "w",encoding='utf-8')    
    file.write(art+"\n")
    os.chdir(dirActual)

    # Taggeo y estructuracion
    out = callTreeTagger(entrada, dirEntradaSalida, dirActual)
    formas,lemas, tags = estructurarTagged(out)

    # convierto a utf-8 para salida sin errores
    formas2=[]
    lemas2=[]
    for x in formas:
        y=x.decode("utf-8")
        formas2.append(y)    
    for x in lemas:
        y=x.decode("utf-8")
        lemas2.append(y)        
    for x in tags:
        y=x.decode("utf-8")
    #agrego
    formasFinal.append(vector2paragraph(formas2))
    lemasFinal.append(vector2paragraph(lemas2))
    tagsFinal.append(vector2paragraph(tags))
# despliego resultados
output_table = DataFrame({
                'formas':formasFinal,
                'lemas':lemasFinal,
                'Tag':tagsFinal,
                })
