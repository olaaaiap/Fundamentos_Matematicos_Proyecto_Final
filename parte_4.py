import poligono as plg


#cargar la lista de vértices y nombres de los archivos
listaVertices, listaNombres  = plg.cargarListaVertices("helpers/verticesFiguras.json")


for i, vertices in enumerate(listaVertices):
    nombre_archivo = listaNombres[i]
    polig = plg.Poligono(vertices)

    triangulos = polig.earClipping() #calcular la triangulación para calcular el área
    print(f"Area de {nombre_archivo}: {polig.calcularArea(triangulos)}")

