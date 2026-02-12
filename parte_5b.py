import poligono as plg

listaVertices, listaNombres = plg.cargarListaVertices("helpers/verticesFiguras.json")

for i, vertices in enumerate(listaVertices, start=1):
    nombre_archivo = listaNombres[i-1]+"_envolvente_convexa"
    polig = plg.Poligono(vertices)
    # envConv = polig.envolventeConvexaGraham()
    envConv = polig.envolventeConvexaGrahamMejorado()
    polig.dibujarEnvolventeConvexa(envConv, carpeta="resultados/parte5b", nombre_archivo=nombre_archivo, guardar=True, enseñar=False )
 
