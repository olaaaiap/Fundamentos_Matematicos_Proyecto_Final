import poligono as plg

#cargar la lista de vértices y nombres de los archivos
listaVertices, listaNombres  = plg.cargarListaVertices("helpers/verticesFiguras.json")

for i, vertices in enumerate(listaVertices):
    nombre_archivo = listaNombres[i]+"_envolvente_convexa"
    polig = plg.Poligono(vertices)
    
    envConv = polig.envolventeConvexaJarvisMejorado() #obtener la env. conv. con el algoritmo de Jarvis mejorado
    polig.dibujarEnvolventeConvexa(envConv, carpeta="resultados/parte5a", nombre_archivo=nombre_archivo, guardar=True, enseñar=False )
 
   
