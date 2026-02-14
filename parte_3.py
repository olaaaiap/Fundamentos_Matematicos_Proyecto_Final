import poligono as plg


listaVertices, listaNombres = plg.cargarListaVertices("helpers/verticesFiguras.json")



for i, vertices in enumerate(listaVertices, start=1):
    nombre_archivo = listaNombres[i-1] + "_triangulacion"
    polig = plg.Poligono(vertices)

    triangulos = polig.earClipping()
    polig.dibujarTriangulacion(triangulos, carpeta="resultados/parte3", nombre_archivo=nombre_archivo, guardar=True, enseñar=False)
    
