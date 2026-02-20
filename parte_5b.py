import poligono as plg

#cargar la lista de vértices y nombres de los archivos
listaVertices, listaNombres = plg.cargarListaVertices("helpers/verticesFiguras.json")

for i, vertices in enumerate(listaVertices):
    nombre_archivo = listaNombres[i]+"_envolvente_convexa"
    polig = plg.Poligono(vertices)
    
    envConv = polig.envolventeConvexaGrahamMejorado() #obtener la env. conv. con el algoritmo de Graham mejorado
    polig.dibujarEnvolventeConvexa(envConv, carpeta="resultados/parte5b", nombre_archivo=nombre_archivo, guardar=True, enseñar=False )
 
