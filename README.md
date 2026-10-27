# Fundamentos matemáticos - Proyecto final

**Clase `Poligono` en Python con algoritmos de geometría computacional: punto en polígono, triangulación, cálculo de área y envolvente convexa.**

Es el proyecto final de la asignatura de Fundamentos Matemáticos del máster. Se ha desarrollado una clase `Poligono` sobre la que se pueden ejecutar algoritmos geométricos, como el cálculo de la envolvente convexa, la triangulación o el área. Varias de las funciones son versiones mejoradas de algoritmos base.

## Enlaces

- 🎥 **Vídeo de demostración:** [youtu.be/Ctcd2lAr9gM](https://youtu.be/Ctcd2lAr9gM)

## Algoritmos implementados

| Función | Qué hace | Técnica |
|---|---|---|
| `contieneMejorado` | Determina si un punto está dentro del polígono | Raycasting |
| `earClipping` | Triangula el polígono | Ear Clipping |
| `hayVerticeDentro` | Comprueba si algún vértice cae dentro de un triángulo | Comparación de áreas |
| `hayVerticeDentroMejorado` | Igual que la anterior, en versión mejorada | Orientación |
| `calcularArea` | Calcula el área total de una lista de triángulos | Suma de áreas |
| `calcularAreaTriangulo` | Calcula el área de un triángulo | — |
| `envolventeConvexaJarvisMejorado` | Calcula la envolvente convexa | Jarvis (Gift Wrapping) |
| `envolventeConvexaGrahamMejorado` | Calcula la envolvente convexa | Graham |

## Detalle de las funciones

### Punto en polígono

#### `contieneMejorado(self, punto)`

Es la versión mejorada de `contiene(self, punto)`. Usa un algoritmo de raycasting mejorado para determinar si un punto está dentro del polígono: lanza un rayo horizontal hacia la derecha y cuenta los cruces. Si la cantidad es impar, devuelve `True`.

- **Parámetros:** `punto`, el punto (x, y).
- **Devuelve:** `True` si el punto está dentro del polígono.
- **Referencia:** [Check if a point belongs to a polygon](https://notes.suhaib.in/docs/code/geometry/theory/check-if-a-point-belongs-to-a-polygon/)

### Triangulación

#### `earClipping(self)`

Algoritmo que encuentra la triangulación de un polígono con la técnica de Ear Clipping.

- **Devuelve:** una lista de triángulos, cada uno con 3 vértices.

#### `hayVerticeDentro(listaVertices, v_prev, v_i, v_next)`

Algoritmo que comprueba si hay algún vértice dentro del triángulo formado por `v_prev`, `v_i` y `v_next`.

- **Parámetros:**
  - `listaVertices`: lista de vértices del polígono.
  - `v_prev`, `v_i`, `v_next`: vértices del triángulo.
- **Devuelve:** `True` si hay un vértice dentro del triángulo y `False` si no lo hay.
- **Referencia:** [Check if a point is in a 2D triangle](https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle) (*Triangles area approach*)

#### `hayVerticeDentroMejorado(listaVertices, v_prev, v_i, v_next)`

Versión mejorada de la anterior. También comprueba si hay algún vértice dentro del triángulo formado por `v_prev`, `v_i` y `v_next`.

- **Parámetros:**
  - `listaVertices`: lista de vértices del polígono.
  - `v_prev`, `v_i`, `v_next`: vértices del triángulo.
- **Devuelve:** `True` si hay un vértice dentro del triángulo y `False` si no lo hay.
- **Referencia:** [Check if a point is in a 2D triangle](https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle) (*Orientation approach*)

### Área

#### `calcularArea(self, triangulos)`

Algoritmo que calcula el área total de una secuencia de triángulos.

- **Parámetros:** `triangulos`, una lista de triángulos con 3 vértices cada uno.
- **Devuelve:** el área total de los triángulos.

#### `calcularAreaTriangulo(punto1, punto2, punto3)`

Algoritmo que calcula el área de un triángulo.

- **Parámetros:** `punto1`, `punto2` y `punto3`, los 3 vértices del triángulo.
- **Devuelve:** el área del triángulo.

### Envolvente convexa

#### `envolventeConvexaJarvisMejorado(self)`

Es la versión mejorada de `envolventeConvexaJarvis(self)`. Encuentra la envolvente convexa con la técnica de Jarvis.

- **Devuelve:** el polígono de la envolvente convexa.

#### `envolventeConvexaGrahamMejorado(self)`

Es la versión mejorada de `envolventeConvexaGraham(self)`. Encuentra la envolvente convexa con la técnica de Graham.

- **Devuelve:** el polígono de la envolvente convexa.

### Otros algoritmos

Hay otros algoritmos, como los de dibujado o carga de datos, que no se describen en este README porque no forman parte de la clase `Poligono` o no son lo suficientemente relevantes. Para más detalles, se pueden consultar el código y sus comentarios.

## Tecnologías

- **Python**


## Autora

Olaia Picabea
