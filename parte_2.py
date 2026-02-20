import poligono as plg
from shapely.geometry import Point, Polygon
import random

#cargar la lista de vértices y nombres de los archivos
listaVertices, listaNombres = plg.cargarListaVertices("helpers/verticesFiguras.json")

for i, vertices in enumerate(listaVertices):
    nombre_archivo = listaNombres[i]
    polig = plg.Poligono(vertices)
    polygonShapely = Polygon(vertices) #crear el poligono en shapely para comparar resultados

    #Calcular los x e y mínimos y máximos para generar un punto cerca del polígono
    min_x = min([p[0] for p in vertices])
    max_x = max([p[0] for p in vertices])
    min_y = min([p[1] for p in vertices])
    max_y = max([p[1] for p in vertices])


    # Generar 10 puntos aleatorios
    for j in range(10):
        punto = (random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        print(f"PUNTO: {punto}")

        dentro=polig.contieneMejorado(punto) #comprobar si está dentro del polígono con mi función

        ########## COMPARAR CON SHAPELY ##########
        point = Point(punto[0], punto[1])
        dentroShapely = polygonShapely.contains(point) #comprobar si está dentro del polígono con shapely
        ########## END COMPARAR CON SHAPELY ######


        if(dentro != dentroShapely): #si los resultados no coincide, imprimir un mensaje de error
            print(f"Error en {nombre_archivo}: ¡Mi solución y la de Shapely no coinciden!")
        if (j==0): #solo guardar el png del primer punto (para no llenar la carpeta de imágenes)
            polig.dibujarConPunto(punto, dentro, "resultados/parte2", nombre_archivo=nombre_archivo, guardar=True, enseñar=False)
    

