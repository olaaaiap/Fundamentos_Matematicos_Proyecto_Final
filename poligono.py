import numpy as np
import matplotlib.pyplot as plt

import os
import json

#estructura de datos para guardar un poligono: lista de vertices, matrices... lo mas simple es una lista de tuplas

#Ahora tenemos q crear nuestra funcion "contains". 
# cuidado si pisa justo los vertices? buscar en la documentacion, 
# hay metodos. un metodo es mover un poquito el punto 
# (+0,001 por ejemplo. pero cuidado con cuanto lo movemos pq puede traer errores) 
# y hacer otra vez el experimento, pero cuidado si esta muy muy cerca del borde.
#  Otra opcion es lanzar mas de un rayo. 
# Empezar por implementaciones sencillas. 
# pensar en que situaciones puede fallar y en cuales funciona. 
# identificar los casos especiales.
# en el ejemplo de main.py, un punto corta con unos vertices, 
# pero 2 de esos se juntan en una arista horizontal, justo donde iria al raycast horizontal. 
# eso tendriamos que contarlo como 1, no como 2
# mirar los libros de la bibliografia, el segundo libro tiene los algoritmos online.

class Poligono:
    def __init__(self, vertices, name=""):
        self.vertices = vertices
        self.n = len(vertices) #cantidad de vertices
        self.name = name
    
    def __repr__(self):
        pts_str = ", ".join([str(i) for i in self.vertices])
        return f"POLIGONO({self.n})\n{pts_str}\n"
    
    #region PARTE 2 - PUNTO EN POLÍGONO

    def contiene(self, punto):
        """
        Algoritmo de Raycasting para determinar si un punto está dentro del poligono
        Lanzamos un rayo horizontal hacia la derecha

        :param punto: punto (x, y)
        :return True si el punto está dentro del Polígono
        """
        
        cruces = 0 #contador de la cantidad de cruces que ha detectado el rayo
        x, y = punto
        #para cada arista del poligono
        for i in range(self.n):
            x1, y1 = self.vertices[i-1] #en la primera iteracion cogerá el -1, es decir, el ultimo punto
            x2, y2 = self.vertices[i]

            #Detectar y quitar las aristas donde sus dos vértices están a la izquierda del punto a analizar
            if(x1 < x) and (x2 < x):
                continue
            
            #Todas las aristas que uno de sus vértices está debajo del punto podrán cortar con el rayo
            if (y > y1) != (y > y2): 
                #calcular intersección con la fórmula vista en clase
                interseccion_x = x1 + ((y - y1) * (x2 - x1)) / (y2 - y1)

                #Si el componente x calculado es mayor o igual al x del punto, hay intersección y aumentamos el contador de cruces
                if interseccion_x >= x:
                    cruces+=1
        return cruces % 2 == 1 #Si la cantidad de cruces es impar, el punto estará dentro del polígono.
    
    def contieneMejorado(self, punto):
        """
        Algoritmo mejorado de Raycasting para determinar si un punto está dentro del poligono
        Lanzamos un rayo horizontal hacia la derecha

        https://notes.suhaib.in/docs/code/geometry/theory/check-if-a-point-belongs-to-a-polygon/

        :param punto: punto (x, y)
        :return True si el punto está dentro del Polígono
        """
        
        ## Casos controlados:
        ## 1. Que el punto esté exactamente sobre una arista.
        ## 2. Que el punto esté exactamente encima de un vértice.
       

        cruces = 0
        x, y = punto
        
        for i in range(self.n):
            x1, y1 = self.vertices[i-1] 
            x2, y2 = self.vertices[i]

            #Solución del problema 1: punto justo sobre una arista
            epsilon = 1e-9 #Para controlar errores de coma flotante

            vectorU = [x2 - x1, y2 - y1]
            vectorV = [x - x1, y - y1]

            cross_product = np.cross(vectorU, vectorV)

            #Si el punto está muy cerca de la arista
            if abs(cross_product) <= epsilon:
                #comprobar si el punto está dentro del segmento
                if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
                    return True
                

            #Solución del problema 2: punto justo encima de un vértice
            #Si el punto a analizar se encuentra justo encima de un vértice, ese punto se considerará dentro del polígono
            if (x, y) == (x1, y1) or (x,y) == (x2,y2):
                return True

            #Si los dos vértices de la arista están a la izquierda del punto, el rayo no podrá cortarla
            if(x1 < x) and (x2 < x):
                continue
            
            #Todas las aristas que uno de sus vértices está debajo del punto podrán cortar con el rayo
            #Así evitamos que si el rayo pasa justo por un vértice, se cuente como 2 cruces
            if (y > y1) != (y > y2): 
                interseccion_x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)

                if interseccion_x >= x:
                    cruces+=1
        
        return cruces % 2 == 1 
    
    #region PARTE 3 - TRIANGULACIÓN

    def earClipping(self):
        """
        Algoritmo que encontrará la triangulación de un polígono utilizando la técnica de Ear Clipping.

        :return lista de triángulos, donde cada triángulo tendrá 3 vértices
        """
        listaVertices = self.vertices.copy()
        T = []
        while len(listaVertices)>3: #buscamos orejas mientras haya más de 3 vértices
            #Para cada vértice, comprobamos si forma una oreja con sus vecinos.
            for index in range(len(listaVertices)):
                v_i = listaVertices[index]
                v_prev = listaVertices[(index-1)%len(listaVertices)]
                v_next = listaVertices[(index+1)%len(listaVertices)]
                if(ccw(v_prev, v_i, v_next)):
                    #Verificamos que no haya ningún otro vértice dentro de este triángulo
                    if not Poligono.hayVerticeDentroMejorado(listaVertices, v_prev, v_i, v_next):
                        #Se ha encontrado una oreja
                        T.append([v_prev, v_i, v_next])
                        listaVertices.remove(v_i) #eliminamos el vértice de la oreja encontrado, y seguimos buscando más orejas
                        break
        #cuando queden 3 vértices, añadirlos a la lista de triángulos y terminar
        T.append([listaVertices[0], listaVertices[1], listaVertices[2]])
        return T

    def hayVerticeDentro(listaVertices, v_prev, v_i, v_next):
        """
        Algoritmo que comprobará si hay algún vértice dentro del triángulo formado por v_prev, v_i y v_next
        https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle  -  Triangles area approach

        :return True si hay un vértice dentro del triángulo, False si no lo hay
        """
        for v in listaVertices:
            #Ignorar los vértices del propio triángulo
            if v == v_prev or v == v_i or v == v_next:
                continue

            #calcular area de los 3 triangulos y comparar con el area total del triangulo
            area_total = Poligono.calcularAreaTriangulo(v_prev, v_i, v_next)
            area1 = Poligono.calcularAreaTriangulo(v, v_i, v_next)
            area2 = Poligono.calcularAreaTriangulo(v_prev, v, v_next)
            area3 = Poligono.calcularAreaTriangulo(v_prev, v_i, v)
            if abs(area_total - (area1 + area2 + area3)) <= 1e-9: #controlar errores de coma flotante
                return True #Hay un vértice dentro
            
        return False

    def hayVerticeDentroMejorado(listaVertices, v_prev, v_i, v_next):
            """
            Algoritmo mejorado que comprobará si hay algún vértice dentro del triángulo formado por v_prev, v_i y v_next
            https://www.baeldung.com/cs/check-if-point-is-in-2d-triangle  -  Orientation approach


            :return True si hay un vértice dentro del triángulo, False si no lo hay
            """
            # Problema controlado: Si el punto está exactamente en un lado del triángulo o muy cerca del borde puede dar un falso positivo
            
            for v in listaVertices:
                #Ignorar los vértices del propio triángulo
                if v == v_prev or v == v_i or v == v_next:
                    continue

                # Comprobar si v está dentro del triángulo
                # v está dentro si está a la izquierda de cada lado del triángulo
                if (ccw(v_prev, v_i, v) and ccw(v_i, v_next, v) and ccw(v_next, v_prev, v)):
                    return True  #Hay un vértice dentro

            return False
    
    #region PARTE 4 - ÁREA

    def calcularArea(self, triangulos):
        """
        Algoritmo que calculará el area total de una secuencia de triángulos

        :param triangulos: lista de triángulos, donde cada triángulo tendrá 3 vértices
        :return area total de los triángulos
        """
        area = 0 #variable de guardará la suma de los areas de los triángulos
        for triangulo in triangulos:
            a, b, c = triangulo #obtener los 3 vértices del triángulo
            area += Poligono.calcularAreaTriangulo(a, b, c) #Calcular el area de un triángulo
        return area
    
    def calcularAreaTriangulo(punto1, punto2, punto3):
        """
        Algoritmo que calculará el area total de un triángulo

        :param punto1, punto2, punto3: los 3 vértices del triángulo
        :return area del triángulo
        """
        punto1 = np.array(punto1)
        punto2 = np.array(punto2)
        punto3 = np.array(punto3)

        #obtener los vectores u y v 
        vectorU = [punto2[0] - punto1[0], punto2[1] - punto1[1]] 
        vectorV = [punto3[0] - punto1[0], punto3[1] - punto1[1]] 

        #calcular el area a través del producto vectorial de u y v, y dividirlo entre 2
        return abs(np.cross(vectorU, vectorV)) / 2

    #region PARTE 5A - ENVOLVENTE CONVEXA: JARVIS 

    def envolventeConvexaJarvis(self):
        """
        Algoritmo que encontrará la envolvente convexa utilizando la técnica de Jarvis.
        
        :return: polígono de la envolvente convexa.
        """

        envConv = []
        #encontrar punto más a la izquierda
        p1 = min(self.vertices)
        indexP1 = self.vertices.index(p1)
        
        #guardar ese punto en la envolvente convexa
        pHelper = indexP1

        while (True):
            envConv.append(pHelper)

            #Coger el siguiente punto en la lista. Si llega al final de la lista, volverá al inicio
            p2 = (pHelper + 1) % len(self.vertices) 

            for i in range(len(self.vertices)):
                if i == pHelper: #Si el punto a analizar es el mismo que el punto de referencia, no lo analizamos
                    continue
                #Si el giro pHelper, i, p2 es en sentido antihorario, entonces el punto i es un mejor candidato que p2
                if ccw(self.vertices[pHelper], self.vertices[i], self.vertices[p2]): 
                    p2 = i

            pHelper = p2 #asignar a pHelper el mejor punto encontrado, y añadirlo a la envolvente convexa

            #Si llegamos al inicio de la envolvente convexa, terminar
            if(pHelper==indexP1):
                break
        
        #Crear el polígono con la envolvente convexa
        poligonoRet= Poligono([self.vertices[i] for i in envConv])
        return poligonoRet

    def envolventeConvexaJarvisMejorado(self):
        """
        Algoritmo mejorado que encontrará la envolvente convexa utilizando la técnica de Jarvis.
        
        :return: polígono de la envolvente convexa.
        """
        ##Casos controlados:
        ##  1. Que haya puntos duplicados en la lista de vertices
        ##  2. Que el polígono tenga 3 o menos vértices
        
        #Si tiene menos de 3 vertices, devolver tal cual
        if len(self.vertices) <= 3:
            return Poligono(self.vertices)    
              
        #Eliminar duplicados
        vertices_unicos = []
        for v in self.vertices:
            if v not in vertices_unicos:
                vertices_unicos.append(v)


        envConv = []
        #encontrar punto más a la izquierda
        p1 = min(vertices_unicos)
        indexP1 = vertices_unicos.index(p1)
        
        #guardar ese punto en la envolvente convexa
        pHelper = indexP1

        while (True):
            envConv.append(pHelper)

            #Coger el siguiente punto en la lista. Si llega al final de la lista, volverá al inicio
            p2 = (pHelper + 1) % len(vertices_unicos) 

            for i in range(len(vertices_unicos)):
                if i == pHelper: #Si el punto a analizar es el mismo que el punto de referencia, no lo analizamos
                    continue
                #Si el giro pHelper, i, p2 es en sentido antihorario, entonces el punto i es un mejor candidato que p2
                if ccw(vertices_unicos[pHelper], vertices_unicos[i], vertices_unicos[p2]): 
                    p2 = i

            pHelper = p2 #asignar a pHelper el mejor punto encontrado, y añadirlo a la envolvente convexa

            #Si llegamos al inicio de la envolvente convexa, terminar
            if(pHelper==indexP1):
                break
        
        #Crear el polígono con la envolvente convexa
        poligonoRet= Poligono([vertices_unicos[i] for i in envConv])
        return poligonoRet
    

        envConv = []
        #encontrar punto más a la izquierda
        p1 = min(vertices_unicos)
        indexP1 = vertices_unicos.index(p1)
        
        pHelper = indexP1

        while (True):
            envConv.append(pHelper)

            p2 = (pHelper + 1) % len(vertices_unicos) 

            for i in range(len(vertices_unicos)):
                if i == pHelper:
                    continue
                if ccw(vertices_unicos[pHelper], vertices_unicos[i], vertices_unicos[p2]):
                    p2 = i

            pHelper = p2


            if(pHelper==indexP1):
                break
        
        # return envConv
        poligonoRet= Poligono([vertices_unicos[i] for i in envConv])
        return poligonoRet

    #region PARTE 5B - ENVOLVENTE CONVEXA: GRAHAM 

    def envolventeConvexaGraham(self):
        """
        Algoritmo que encontrará la envolvente convexa utilizando la técnica de Graham.
        
        :return: polígono de la envolvente convexa.
        """

        #Ordenar los puntos por la coordenada x
        puntos_ordenados = sorted(self.vertices)

        #Poner los puntos p1 y p2 en una lista L_upper, donde p1 es el primer punto
        p1= puntos_ordenados[0]
        p2= puntos_ordenados[1]
        L_upper = [p1, p2]

        for i in range (2, len(puntos_ordenados)):
            L_upper.append(puntos_ordenados[i])
            #mientras que L_upper contenga más de 2 puntos y los últimos 3 puntos de L_upper no formen un giro en sentido antihorario...
            while (len(L_upper) > 2 and not ccw(L_upper[-3], L_upper[-2], L_upper[-1])):
                L_upper.pop(-2) #... eliminar el punto del medio

        #poner los puntos pn y pn-1 en una lista L_lower donde pn es el primer punto
        L_lower = [puntos_ordenados[-1],puntos_ordenados[-2]]

        #para cada punto desde el penúltimo hasta el primero
        for i in reversed(range(len(puntos_ordenados) - 2)):
            L_lower.append(puntos_ordenados[i])
            #mientras que L_lower contenga más de 2 puntos y los últimos 3 puntos de L_lower no formen un giro en sentido antihorario...
            while (len(L_lower)>2 and not ccw(L_lower[-3], L_lower[-2], L_lower[-1])):
                L_lower.pop(-2) #... eliminar el punto del medio
        
        #quitar el primer y ultimo punto de L_lower para evitar vertices duplicados
        L_lower.pop(-1)
        L_lower.pop(0)

        #Juntar L_lower y L_upper
        L = L_upper + L_lower

        poligonoRet = Poligono(L)
        return poligonoRet
    
    def envolventeConvexaGrahamMejorado(self):
        """
        Algoritmo mejorado que encontrará la envolvente convexa utilizando la técnica de Graham.
        
        :return: polígono de la envolvente convexa.
        """

        ##Casos controlados:
        ##  1. Que haya puntos duplicados en la lista de vertices
        ##  2. Que el polígono tenga 3 o menos vértices
        
        #Si tiene menos de 3 vertices, devolver tal cual
        if len(self.vertices) <= 3:
            return Poligono(self.vertices)    
              
        #Eliminar duplicados
        vertices_unicos = []
        for v in self.vertices:
            if v not in vertices_unicos:
                vertices_unicos.append(v)

        #Ordenar los puntos por la coordenada x
        puntos_ordenados = sorted(vertices_unicos)

        #Poner los puntos p1 y p2 en una lista L_upper, donde p1 es el primer punto
        p1= puntos_ordenados[0]
        p2= puntos_ordenados[1]
        L_upper = [p1, p2]

        for i in range (2, len(puntos_ordenados)):
            L_upper.append(puntos_ordenados[i])
            #mientras que L_upper contenga más de 2 puntos y los últimos 3 puntos de L_upper no formen un giro en sentido antihorario...
            while (len(L_upper) > 2 and not ccw(L_upper[-3], L_upper[-2], L_upper[-1])):
                L_upper.pop(-2) #... eliminar el punto del medio

        #poner los puntos pn y pn-1 en una lista L_lower donde pn es el primer punto
        L_lower = [puntos_ordenados[-1],puntos_ordenados[-2]]

        #para cada punto desde el penúltimo hasta el primero
        for i in reversed(range(len(puntos_ordenados) - 2)):
            L_lower.append(puntos_ordenados[i])
            #mientras que L_lower contenga más de 2 puntos y los últimos 3 puntos de L_lower no formen un giro en sentido antihorario...
            while (len(L_lower)>2 and not ccw(L_lower[-3], L_lower[-2], L_lower[-1])):
                L_lower.pop(-2) #... eliminar el punto del medio
        
        #quitar el primer y ultimo punto de L_lower para evitar vertices duplicados
        L_lower.pop(-1)
        L_lower.pop(0)

        #Juntar L_lower y L_upper
        L = L_upper + L_lower

        poligonoRet = Poligono(L)
        return poligonoRet

    
    ######################### FUNCIONES DE DIBUJADO #########################
    
    def dibujar(self, carpeta="", nombre_archivo="", guardar=False, enseñar=True):
        """
        Algoritmo que dibujará el polígono en una ventana.
        """
        xs = [p[0] for p in self.vertices]
        ys = [p[1] for p in self.vertices]
        plt.scatter(xs, ys, color='blue', label='Puntos') #pintar los vértices
        
        lineas = self.vertices.copy() #hacer copia de los vertices para no cambiar el original
        lineas.append(lineas[0]) #añadimos el primer vértice para cerrar el polígono

        cx = [p[0] for p in lineas]
        cy = [p[1] for p in lineas]

        plt.plot(cx, cy, color='green', linewidth=2, label='') #pintar las aristas

        if guardar: #guardar el png en la carpeta especificada
            ruta = os.path.join(carpeta, nombre_archivo)
            plt.savefig(ruta)  
            plt.close()
        if enseñar:
            plt.show()

    def dibujarConPunto(self, punto, dentro, carpeta="", nombre_archivo="", guardar=False, enseñar=True):
        """
        Algoritmo que dibujará el polígono y el punto en una ventana.

        :param punto: punto que se dibujará
        :param dentro: booleano que dará la información de que si el punto está o no dentro del poligono
        :param carpeta: nombre de la carpeta donde se guardará la imagen.
        :param nombre_archivo: nombre con el que se guardará el archivo
        :param guardar: booleano que indicará si se guardará la imagen o no
        :param enseñar: booleano que indicará si se mostrará la imagen en una ventana o no
        """

        nombre_archivo = nombre_archivo + ".png"

        # Crear la carpeta si no existe
        if(guardar):
            os.makedirs(carpeta, exist_ok=True)

        xs = [p[0] for p in self.vertices]
        ys = [p[1] for p in self.vertices]
        plt.scatter(xs, ys, color='blue', label='') #pintar los vértices
        
        lineas = self.vertices.copy() #hacer copia de los vertices para no cambiar el original
        lineas.append(lineas[0]) #añadimos el primer vértice para cerrar el polígono

        cx = [p[0] for p in lineas]
        cy = [p[1] for p in lineas]

        color = 'green' if dentro else 'red' #si el punto está dentro del polígono, pintar de verde, si no, de rojo
        plt.scatter([punto[0]], [punto[1]], color=color, s=50, label='Punto')
            
        plt.plot(cx, cy, color='green', linewidth=2, label='') #pintar las aristas

        if guardar: #guardar el png en la carpeta especificada
            ruta = os.path.join(carpeta, nombre_archivo)
            plt.savefig(ruta)  
            plt.close()
        if enseñar:
            plt.show()
    
    def dibujarEnvolventeConvexa(self, envolvente_poligono, carpeta="", nombre_archivo="", guardar=False, enseñar=True):
        """
        Algoritmo que dibujará el polígono con su envolvente convexa

        :param envolvente_poligono: polígono que representa la envolvente convexa.
        :param carpeta: nombre de la carpeta donde se guardará la imagen.
        :param nombre_archivo: nombre con el que se guardará el archivo
        :param guardar: booleano que indicará si se guardará la imagen o no
        :param enseñar: booleano que indicará si se mostrará la imagen en una ventana o no
        """
        
        nombre_archivo = nombre_archivo + ".png"

        #Crear la carpeta si no existe
        if(guardar):
            os.makedirs(carpeta, exist_ok=True)


        #Guardar los índices de la env. convexa para pintar esos vértices de un color diferente
        envolvente_indices = [self.vertices.index(v) for v in envolvente_poligono.vertices]
        indices_envolvente = set(envolvente_indices)

        #Guardar los restantes
        indices_restantes = []
        for i in range(len(self.vertices)):
            if i not in indices_envolvente:
                indices_restantes.append(i)
        
        #Dibujar los puntos de la env. convexa en azul
        xs_env = [self.vertices[i][0] for i in envolvente_indices]
        ys_env = [self.vertices[i][1] for i in envolvente_indices]
        plt.scatter(xs_env, ys_env, color='blue', label='Puntos envolvente')

        #Dibujar los demás puntos en morado
        xs_rest = [self.vertices[i][0] for i in indices_restantes]
        ys_rest = [self.vertices[i][1] for i in indices_restantes]
        plt.scatter(xs_rest, ys_rest, color='purple', label='Otros puntos')
        
        lineas = self.vertices.copy()
        lineas.append(lineas[0]) #Añadir el primer vértice

        cx = [p[0] for p in lineas]
        cy = [p[1] for p in lineas]

        plt.plot(cx, cy, color='green', linewidth=2, label='') #dibujar las aristas

        #dibujar las aristas de la envolvente convexa en rojo
        convexa = [self.vertices[i] for i in envolvente_indices]
        convexa.append(convexa[0])

        cx = [p[0] for p in convexa]
        cy = [p[1] for p in convexa]

        plt.plot(cx, cy, color='red', linewidth=2, label='Envolvente convexa')

        #añadir etiquetas a los vértices de la envolvente convexa
        for (x, y) in convexa:
            plt.text(x + 0.05, y + 0.05, f"({x}, {y})", fontsize=9)

        plt.axis('equal')
        plt.legend()
        plt.title('Polígono y Envolvente Convexa')
        if(guardar):
            ruta = os.path.join(carpeta, nombre_archivo)
            plt.savefig(ruta)  
            plt.close()
        if enseñar:
            plt.show()

    def dibujarTriangulacion(self, triangulos, carpeta, nombre_archivo, guardar=False, enseñar=True ):
        """
        Algoritmo que dibujará el polígono con su triangulación

        :param triangulos: lista de triángulos que forman la triangulación.
        :param carpeta: nombre de la carpeta donde se guardará la imagen.
        :param nombre_archivo: nombre con el que se guardará el archivo
        :param guardar: booleano que indicará si se guardará la imagen o no
        :param enseñar: booleano que indicará si se mostrará la imagen en una ventana o no
        """
            
        nombre_archivo = nombre_archivo + ".png"

        if guardar:
            # Crear la carpeta si no existe
            os.makedirs(carpeta, exist_ok=True)

        #Dibujar el polígono original
        lineas = self.vertices.copy() #hacer copia de los vertices para no cambiar el original
        lineas.append(lineas[0]) #añadimos el primer vértice para cerrar el polígono

        xs = [p[0] for p in lineas]
        ys = [p[1] for p in lineas]

        plt.plot(xs, ys, color='black', linewidth=2, label='Polígono')

        #Dibujar triangulos
        for tri in triangulos:
            for i in range(3): #dibujar cada arista del triángulo
                p1 = tri[i]
                p2 = tri[(i + 1) % 3]
                plt.plot(
                    [p1[0], p2[0]],
                    [p1[1], p2[1]],
                    linestyle='--',
                    color='blue',
                    linewidth=1
                )

        plt.axis('equal')
        plt.title('Triangulación por Ear Clipping')
        if enseñar:
            plt.show()
        if guardar:
            ruta = os.path.join(carpeta, nombre_archivo)
            plt.savefig(ruta)  
            plt.close()



def cargar_interesting_figure_archive(carpeta):
    """
    Algoritmo que devuelve la lista de figuras de los polígonos de Interesting Figure Archive.

    :param carpeta: ruta de la carpeta que contiene los jsons.
    :return figuras: lista de figuras con 2 subobjetos: nombre y vertices.
    """

    figuras = []

    #leemos cada json de la carpeta y guardamos su nombre y vértices en una lista de figuras
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".json"):
            ruta = os.path.join(carpeta, archivo)
            nombre_figura = os.path.splitext(archivo)[0]

            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)

                vertices = [tuple(v) for v in data[0]]

                figuras.append({"nombre": nombre_figura, "vertices": vertices})


    return figuras

def ccw(punto1, punto2, punto3):
    """
    Algoritmo que recibiendo 3 puntos determina si el giro punto1, punto2, punto3 está en sentido anti-horario.

    :param punto1: punto (x, y)
    :param punto2: punto (x, y)
    :param punto3: punto (x, y)
    :return True si el giro está en sentido anti-horario
    """
    punto1 = np.array(punto1)
    punto2 = np.array(punto2)
    punto3 = np.array(punto3)

    vectorU = [punto2[0] - punto1[0], punto2[1] - punto1[1]] #el del final menos el primero.
    vectorV = [punto3[0] - punto1[0], punto3[1] - punto1[1]] #el del final menos el primero. 

    #calcular el producto vectorial de u y v
    crossProduct = np.cross(vectorU, vectorV)
    if(crossProduct > 0):
        return True
    if(crossProduct == 0): #Los tres puntos están alineados
        #En este caso el dot product es equivalente a la distancia al cuadrado. 
        # Por tanto, comparar la distancia al cuadrado entre los puntos nos vale para saber cual está más lejos
        return np.dot(punto2 - punto1, punto2 - punto1) > np.dot(punto3 - punto1, punto3 - punto1) #coger el punto mas lejano
    return False

def guardarListaFiguras(listaFiguras, ruta_archivo):
    """
    Algoritmo que recibiendo la lista de figuras y el nombre de la ruta, guarda su información en json que se utilizará en los ejercicios

    :param listaFiguras: lista de figuras a guardar
    :param ruta_archivo: ruta del archivo donde se debe guardar la información
    """
    #Por cada figura guardar su nombre y vertices en un diccionario
    data=[]
    for figura in listaFiguras:
        data.append({
            "nombre": figura["nombre"],
            "vertices": [list(v) for v in figura["vertices"]]
        })
    

    #crear directorio si no existe
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

    #volcar los datos en un json
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def cargarListaVertices(ruta_archivo):
    """
    Algoritmo que recibiendo la ruta de un archivo json con información de figuras, devuelve las listas de vértices y nombres.

    :param ruta_archivo: ruta del archivo json con la información de las figuras
    :return vertices: lista de listas de vértices, donde cada sublista corresponde a una figura
    :return nombres: lista de nombres de las figuras, donde cada nombre corresponde a una figura
    """

    #abrir archivo y cargar su información
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        data = json.load(f)

    vertices = []
    nombres = []
    
    for figura in data:
        #Convertir cada vértice a tupla
        vertices.append([tuple(v) for v in figura["vertices"]])
        nombres.append(figura["nombre"])

    return vertices, nombres



#region PARTE 1: cargar y guardar los polígonos
listaFiguras = cargar_interesting_figure_archive("./figures")
guardarListaFiguras(listaFiguras, "helpers/verticesFiguras.json")

#Guardar cada figura en png
for i, figura in enumerate(listaFiguras, start=1):
    poligono = Poligono(figura["vertices"], figura["nombre"])
    poligono.dibujar("resultados/parte1", figura["nombre"], guardar=True, enseñar=False)



