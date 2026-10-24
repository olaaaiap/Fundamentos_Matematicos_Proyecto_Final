VIDEO

https://youtu.be/Ctcd2lAr9gM


# Fundamentos matemáticos - proyecto final
  
  En este proyecto final se ha desarrollado una clase Poligono donde se podrán ejecutar algoritmos geométricos como el calculo de la envolvente convexa, triangulación, área etc. 
  Para ello se han desarrollado las siguientes funciones:

#### contieneMejorado(self, punto): versión mejorada de contiene(self, punto) 

Algoritmo mejorado de Raycasting para determinar si un punto está dentro del polígono. Lanzamos un rayo horizontal hacia la derecha y detectamos la cantidad de cruces que hay. Si la cantidad es impar, devolverá True.

 Referencia al recurso utilizado:
 
https://notes.suhaib.in/docs/code/geometry/theory/check-if-a-point-belongs-to-a-polygon/

  
##### Parámetros
- punto: punto (x, y)

##### Devuelve
- True si el punto está dentro del Polígono

    

#### earClipping(self)

Algoritmo que encontrará la triangulación de un polígono utilizando la técnica de Ear Clipping.


##### Devuelve
- Lista de triángulos, donde cada triángulo tendrá 3 vértices


#### hayVerticeDentro(listaVertices, v_prev, v_i, v_next)

Algoritmo que comprobará si hay algún vértice dentro del triángulo formado por v_prev, v_i y v_next.


Referencia al recurso utilizado:
 
https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle - Triangles area approach

  
##### Parámetros
- listaVertices: lista de vértices del polígono.
- v_prev, v_i, v_next: vértices del triángulo

##### Devuelve
- True si hay un vértice dentro del triángulo, False si no lo hay

#### hayVerticeDentroMejorado(listaVertices, v_prev, v_i, v_next)

Algoritmo mejorado que comprobará si hay algún vértice dentro del triángulo formado por v_prev, v_i y v_next.

https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle - Orientation approach

  
##### Parámetros
- listaVertices: lista de vértices del polígono.
- v_prev, v_i, v_next: vértices del triángulo
  

##### Devuelve
- True si hay un vértice dentro del triángulo, False si no lo hay


#### calcularArea(self, triangulos)
Algoritmo que calculará el área total de una secuencia de triángulos

  
##### Parámetros
- triangulos: lista de triángulos, donde cada triángulo tendrá 3 vértices
  

##### Devuelve
- Área total de los triángulos

  
#### calcularAreaTriangulo


Algoritmo que calculará el área total de un triángulo

  
##### Parámetros
- punto1, punto2, punto3: los 3 vértices del triángulo
  

##### Devuelve
- Área del triángulo

#### envolventeConvexaJarvisMejorado(self): versión mejorada de envolventeConvexaJarvis(self)

Algoritmo mejorado que encontrará la envolvente convexa utilizando la técnica de Jarvis.


##### Devuelve
- Polígono de la envolvente convexa.



#### envolventeConvexaGrahamMejorado(self): versión mejorada de envolventeConvexaGraham(self)

Algoritmo mejorado que encontrará la envolvente convexa utilizando la técnica de Graham.

##### Devuelve
- Polígono de la envolvente convexa.


### Otros algoritmos

Hay otros algoritmos como las de dibujado o carga de datos que no se han descrito en este Readme, ya que no son parte de la clase Poligono, o no son lo suficientemente relevantes. Para más detalles analizar el código y sus comentarios.


## Recursos utilizados

https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle

https://notes.suhaib.in/docs/code/geometry/theory/check-if-a-point-belongs-to-a-polygon/

Apuntes y explicaciones que se han visto en clase.

## Autora


Olaia Picabea
