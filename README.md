Clasificación automatica de articulos
 
Esta aplicacion cuenta con 3 funcionalidades:

1. Obtiene articulos de paginas web que tengan un patron scraping (esto es, que tenga un patron inicial y final determinable para cada cuerpo de cada articulo, y por las que se puede navegar entre listas de resultados).

2. Provee algunos metodos de analisis morfologico: 
	+ Etiquetado gramatical a traves de  TNT tagger
	+ Determina que palabras no fueron reconocidas por TNT tagger y permite agregarlas.	
	+ Obtiene contextos (vecindarios) de un pivote (palabra interes)
	+ Obtiene frecuencias de aquellas palabras vecinas a un pivote y les asigna un valor en funcion de su cercania.
	+ Obtiene los n-nomios de un texto. Ejemplo articulo+sustantivo+verbo: el perro corrió.
	 
3. Clasifica articulos
	+ Provee interfaz para ingresar categorias y criterios de clasificacion
	+ Obtiene los resultados en una salida de excel una matriz con 2 columnas: urlArticulo y resultadoClasificacion.

***************************************** ANTES DE INICIAR *****************************************

En "Esquema de comunicaciones.png" se puede ver detalladamente las partes que conforman la aplicación. de aqui se resalta:

- TNT tagger: Herramienta que obtiene las categorias gramaticales y los lemas para cada palabra en un archivo de texto. El programa espera que la salida de tnt tagget sea puesta en la carpeta del codigo con el nombre "<#>Url", donde  <#> se refiere al topeMaximo (vease "procesaHTML.py")
A traves del siguiente link puede usar el servicio de TNT tagger: 
http://grupotnt.udea.edu.co/scripts/cgi-bin/TNTagger/tntag.py

-Analisis.xls: Es una plantilla mas del lado del linguista computacional (analisis morfologico). Aqui se establecen las categorias gramaticales innecesarias, y aquellos lemas que deseen agregarse al no ser reconocidos por TNT tagger. 

-ClasificacionExpresiones.xls: Es una plantilla mas del lado del usuario, o investigador (clasificacion de articulos). Aqui se establecen los tipos de clasificacion y los criterios con los cuales se realizará la clasificacion de articulos. Vale comentar que estos criterios pueden ser obtenidos atraves de algunos metodos de "AnalisisMorfologico.py" como frecuenciasRelativasPonderadas, getTodosContextos, etc.


ERRORES COMUNES:
Si presenta error en el import:  "from operator import itemgetter", debe darle ignorar, parece ser un conflicto cuando se tienen python 2 y 3 ambos instalados.

Al agregar modificar los archivos de excel (por ejemplo para agregar o quitar categorias de clasificacion) se deben modificar los scripts donde se utilicen dichos archivos, pues la asignacion de columnas por leer debe cambiar.

La aplicacion sobreescribe los resultados que genera, por tanto se debe verificar que el archivo a utilizar haya sido generado completamente. Ademas de recordar guardar o cambiar el nombre a aquellos archivos que considera utiles a futuro. 

***************************************** CREDITOS *****************************************
Jason E. Angel 	ajason08@gmail.com	Desarrollador
Joan Rodriguez	armj.36@gmail.com	Desarrollador
Jorge Mejia	Instituto Filosofia, udea.	Asesor
 
TNTagger [en línea]. Medellín: Grupo de Investigación TNT, Escuela de Idiomas, Universidad de Antioquia. . [30/07/15]. [http://grupotnt.udea.edu.co/TNTagger].

Periodico ejemplo: http://www.elcolombiano.com/
