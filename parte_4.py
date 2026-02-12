import poligono as plg


listaVertices, listaNombres  = plg.cargarListaVertices("helpers/verticesFiguras.json")



for i, vertices in enumerate(listaVertices, start=1):
    nombre_archivo = listaNombres[i-1]
    polig = plg.Poligono(vertices)

    triangulos = polig.earClipping()
    print(f"Area de {nombre_archivo}: {polig.calcularArea(triangulos)}")

