from shapely import Point, Polygon
from shapely.plotting import plot_points, plot_polygon
import matplotlib.pyplot as plt

xy = (3, 4)

vertices = [
    (0, 0),
    (5, 0),
    (5, 5),
    (7, 3),
    (9, 5),
    (11, 5),
    (7, 8),
    (7, 5),
    (5, 11),
    (14, 8),
    (17, 11),
    (17, 5),
    (19, 13),
    (19, 18),
    (17, 18),
    (19, 20),
    (12, 22),
    (14, 16),
    (12, 18),
    (9, 16),
    (9, 20),
    (7, 18),
    (5, 18),
    (7, 16),
    (9, 11),
    (0, 18),
    (5, 8),
    (0, 5),
]


#los agujeros de un poligono se definen en orden horario. No nos hara falta, pero para que lo sepamos
punto = Point(3.2, 5)
poligono = Polygon(vertices)



#Uno de los errores mas comunes en el proyecto final es repetir el primer vertice al final de la lista!
print(poligono.contains(punto))

color="green" if poligono.contains(punto) else "red"
#recomendacion de diego
fig, ax = plt.subplots() #crear figura y ejes
plot_polygon(poligono, ax=ax, facecolor="none") #pasarle los ejes donde quiero q me pinte. facecolor="none" para que no rellene el poligono
plot_points(punto, ax=ax, color=color)
plt.show()

#cuando creamos nuestra clase poligono, hacer que si ejecuto "poligono" imprima POLYGON((3 2, 4 6, 3 8, 3 2)).
#VER poligono.py!!!!