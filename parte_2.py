import poligono as plg
from shapely.geometry import Point, Polygon
import random

listaVertices, listaNombres = plg.cargarListaVertices("helpers/verticesFiguras.json")



for i, vertices in enumerate(listaVertices, start=1):
    nombre_archivo = listaNombres[i-1]
    polig = plg.Poligono(vertices)
    polygonShapely = Polygon(vertices)

    #Calcular los x e y mínimos y máximos para generar un punto cerca del polígono
    min_x = min([p[0] for p in vertices])
    max_x = max([p[0] for p in vertices])
    min_y = min([p[1] for p in vertices])
    max_y = max([p[1] for p in vertices])


    # Generar 10 puntos aleatorios
    for j in range(10):
        punto = (random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        print(f"PUNTO: {punto}")


        dentro=polig.contieneMejorado(punto)

        ########## COMPARAR CON SHAPELY ##########
        point = Point(punto[0], punto[1])
        dentroShapely = polygonShapely.contains(point)
        ########## END COMPARAR CON SHAPELY ######


        if(dentro != dentroShapely):
            print(f"Error en {nombre_archivo}: ¡Mi solución y la de Shapely no coinciden!")
        if (j==0):
            polig.dibujarConPunto(punto, dentro, "resultados/parte2", nombre_archivo=nombre_archivo, guardar=True, enseñar=False)
    

