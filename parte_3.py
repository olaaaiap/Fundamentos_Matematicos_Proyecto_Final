import poligono as plg

#cargar la lista de vértices y nombres de los archivos
listaVertices, listaNombres = plg.cargarListaVertices("helpers/verticesFiguras.json")


for i, vertices in enumerate(listaVertices):
    nombre_archivo = listaNombres[i] + "_triangulacion"
    polig = plg.Poligono(vertices)

    triangulos = polig.earClipping() #obtener la triangulación del polígono
    polig.dibujarTriangulacion(triangulos, carpeta="resultados/parte3", nombre_archivo=nombre_archivo, guardar=True, enseñar=False)
    
