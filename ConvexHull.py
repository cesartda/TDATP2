# -*- coding: utf-8 -*-
# TP2 TDA Parte 1: El robot y el camino seguro
# Se dan un conjunto de N puntos en un archivo, de los cuales hay uno de inicio
# y uno de fin
# Se pide calcular el camino más corto que recorra sobre la envoltura convexa
# que vaya de inicio a fin.
# Se proponen 3 métodos para calcular la envoltura convexa: A fuerza bruta, con
# Graham scan y con D&C (-F , -G o -D)

import argparse
import math

def main(points_file,M):
    ## Interpreto el archivo
    # En la posición 0 de cada punto está la coordenada X, en la 1 es la Y
    points = read_points(points_file)
    M = "G"
    if M == "F":
        convex_hull = convex_hull_brute(points)
    if M == "G":
        convex_hull = convex_hull_graham(points)
    if M == "D":
        convex_hull = convex_hull_DC(points)
    ## Acá hay que sacar que lado conviene e imprimirlo como pide el enunciado
    print_path(points,convex_hull)

    return 

def read_points(str_file):
    ## Abro el archivo y guardo los puntos en una lista
    points_list = []
    for line in open(str_file, 'r'):
        new_point = []
        for i in line.split(' '):
            new_point.append(float(i))
        points_list.append(new_point)
    return points_list

def convex_hull_graham(points):
    # Busco el punto con coordenada Y mínima (más abajo). En caso de empate es
    # el más a la izquierda (menor X)
    # Ordeno por ángulo, yendo en sentido antihorario tomando como eje el punto
    # de antes
    convex_hull_points = []
    pivot = points[0]
    for i in range(1,len(points)):
        if points[i][1] < pivot[1]:
            pivot = points[i]
        elif points[i][1] == pivot[1] and points[i][0] < pivot[0]:
            pivot = points[i]
    # Ordeno por ángulo
    convex_hull_points.append(pivot)
    # points_full_info tiene posicion en points, el punto en si, cos y modulo
    points_full_info = []
    for i in range(0,len(points)):
        if pivot != points[i]:
            x = (pivot[0] - points[i][0])**2
            y = (pivot[1] - points[i][1])**2
            cos_point = x/(x+y)
            points_full_info.append([i,points[i],cos_point,x+y])
    points_full_info.sort(key=lambda x:x[2])
    # Saco los que tengan el mismo ángulo, me quedo con el de máximo módulo
    # Los dejo en points para no hacerme quilombo con los índices
    i = 1
    while i<len(points_full_info):
        if points_full_info[i][2] == points_full_info[i-1][2]:
            # Igual angulo, me fijo cual de los 2 saco
            if points_full_info[i][3] < points_full_info[i-1][3]:
                points_full_info.pop(i)
            else:
                points_full_info.pop(i-1)
        else:
            # si saco algo, la lista se modifica y no debo avanzar
            i=i+1

    # Ahora voy a ir agregando a la pila y fijándome si no hacen giros al lado
    # contrario. Si lo hacen saco hasta que deje de ocurrir
    # Arranco con los 3 primeros en la pila
    # Voy a usar la lista como stack, ya que agregar o sacar al final son O(1)
    convex_hull_points.append(points_full_info[0][1])
    convex_hull_points.append(points_full_info[1][1])
    for i in range(2,len(points_full_info)):
        current = points_full_info[i][1]
        while cross_product(current,convex_hull_points[-1],convex_hull_points[-2])<0:
            convex_hull_points.pop()
        convex_hull_points.append(current)
    return convex_hull_points

def cross_product(c,b,a):
    # Supongo dos segmentos de recta que van de a hacia c
    cb = [c[0] - b[0],c[1] - b[1]]
    ba = [b[0] - a[0],b[1] - a[1]]
    return (cb[0]*ba[1])-(cb[1]*ba[0])

def print_path(points,hull):
    # En points está en el primero el inicio y el último el de llegada
    # Hago los dos recorridos, y al final compruebo cual tiene menor distancia
    # Se espera que los puntos del hull estén en orden
    print(hull)
    start = points[0]
    finish = points[1]

    st_i =hull.index(start)
    last = hull[st_i]
    st_i = st_i+1
    distance = 0
    path = [last]
    while hull[st_i]!=finish:
        distance += distance_between(last,hull[st_i])
        last = hull[st_i]
        path.append(last)
        st_i = (st_i+1)%len(hull)
    path.append(hull[st_i])
    distance += distance_between(last,hull[st_i])
    print("Camino 1: Longitud " + str(distance))
    print(path)
    distance1 = distance

    st_i =hull.index(start)
    last = hull[st_i]
    st_i = st_i-1
    distance = 0
    path = [last]
    while hull[st_i]!=finish:
        distance += distance_between(last,hull[st_i])
        last = hull[st_i]
        path.append(last)
        st_i = (st_i-1)%len(hull)
    path.append(hull[st_i])
    distance += distance_between(last,hull[st_i])
    distance2 = distance
    print("Camino 2: Longitud " + str(distance))
    print(path)
    print("1" if distance1<distance2 else "2")
    return


def distance_between(a,b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parser.')
    parser.add_argument('file')
    parser.add_argument('method',choices=['F', 'G' , 'D'])
    parsed_args = parser.parse_args()
    points_file = parsed_args.file
    M = parsed_args.method
    main(points_file,M)
