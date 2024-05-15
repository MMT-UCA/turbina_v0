#-----------------------------------------------------------------#
#MÓDULO CAMBER - THICKNESS
#Módulo de cálculo de: curvatura, curvatura máxima, curvatura media, espesor y espesor máximo
#-----------------------------------------------------------------#

#IMPORTS

import pandas as pd
import numpy as np
import Datos
import matplotlib.pyplot as plt

#-----------------------------------------------------------------#
#Función de interpolación lineal
def interpolate_fcn(x_1, y_1, x_2, y_2, x_3):
    if x_1 == x_2 :
        y_3 = y_1
        return y_3
    else:
        y_3 = y_1 + ((y_2 - y_1) / (x_2 - x_1)) * (x_3 - x_1)
        return y_3

#-----------------------------------------------------------------#
#Separación de coordenadas de intradós y extradós
def coordinates_lists(x_coordinates,y_coordinates):
    
    y_ext_list = [y for x, y in zip(x_coordinates, y_coordinates) if y >= 0]
    x_ext_list = [x for x, y in zip(x_coordinates, y_coordinates) if y >= 0]
    y_int_list = [y for x, y in zip(x_coordinates, y_coordinates) if y < 0]
    x_int_list = [x for x, y in zip(x_coordinates, y_coordinates) if y < 0]

    return y_ext_list,y_int_list,x_ext_list,x_int_list

#-----------------------------------------------------------------#
#Intervalo en el que se encuentra el x a interpolar
def interval(x_list, y_list,x):

    if x == 0:
        x_upper = 0
        x_lower = 0
        y_lower = 0
        y_upper = 0

    elif x==1:
        x_upper = 0
        x_lower = 0
        y_lower = 0
        y_upper = 0

    else:

        #Encontrar el valor inmediatamente superior en la lista
        x_upper = min([x_min for x_min in x_list if x_min >= x])

        # Encontrar el valor inmediatamente inferior en la lista
        x_lower = max([x_max for x_max in x_list if x_max <= x])
    
        # Obtener los valores de Cl correspondientes a los alphas encontrados
        y_lower = y_list[x_list.index(x_lower)]
        y_upper = y_list[x_list.index(x_upper)]

    return (x_lower, y_lower), (x_upper, y_upper)

#-----------------------------------------------------------------#
#Función de interpolación, devuelve los y correspondientes a la lista de x. (Se emplea una vez para el intradós y otra para el extradós)
def interpolate_coordinates(x,x_list,y_list):
    
    lower_values, upper_values = interval(x_list, y_list, x)
    x_lower, y_lower = lower_values
    x_upper, y_upper = upper_values
    y_value = interpolate_fcn(x_lower,y_lower,x_upper,y_upper,x)

    return y_value

#-----------------------------------------------------------------#
#Curvatura
def camber(df,x): 

    x_coordinates = df['x']
    y_coordinates = df['y']

    y_ext_list,y_int_list,x_ext_list,x_int_list = coordinates_lists(x_coordinates,y_coordinates)

    y_value_ext = interpolate_coordinates(x,x_ext_list,y_ext_list)
    y_value_int = interpolate_coordinates(x,x_int_list,y_int_list)

    camber_value = (y_value_ext + y_value_int)/2

    return camber_value

#-----------------------------------------------------------------#
#h_c, curvatura máxima
def camber_max(df):

    camber_values = []
    x_values = np.arange(0, 1.05, 0.05)

    for x in x_values:
        camber_value = camber(df,x)
        camber_values.append(camber_value)

    max_camber = max(camber_values)

    return max_camber

#-----------------------------------------------------------------#
#Curvatura media
def camber_med(df):

    camber_values = []
    x_values = np.arange(0, 1.05, 0.05)

    for x in x_values:
        camber_value = camber(df,x)
        camber_values.append(camber_value)

    med_camber = np.mean(camber_values)

    return med_camber

#-----------------------------------------------------------------#
#Espesor
def thickness(df,x): 

    x_coordinates = df['x']
    y_coordinates = df['y']

    y_ext_list,y_int_list,x_ext_list,x_int_list = coordinates_lists(x_coordinates,y_coordinates)

    y_value_ext = interpolate_coordinates(x,x_ext_list,y_ext_list)
    y_value_int = interpolate_coordinates(x,x_int_list,y_int_list)

    thickness_value = y_value_ext - y_value_int

    return thickness_value

#-----------------------------------------------------------------#
#t_c, espesor máximo
def thickness_max(df):

    thickness_values = []
    x_values = np.arange(0, 1.05, 0.05)

    for x in x_values:
        thickness_value = thickness(df,x)
        thickness_values.append(thickness_value)

    max_thickness = max(thickness_values)
    #max_thickness = 0.019965931813841535 * 2 #Valor usado en excel

    return max_thickness

#-----------------------------------------------------------------#
#Grafica la curvatura y el perfil
def plot_camber(df):

    camber_values = []
    x_values = np.arange(0, 1.05, 0.05)

    for x in x_values:
        camber_value = camber(df,x)
        camber_values.append(camber_value)

    x_coordinates_airfoil = df['x']
    y_coordinates_airfoil = df['y']
   
    plt.scatter(x_values, camber_values, color='cornflowerblue', label='Camber')
    plt.scatter(x_coordinates_airfoil, y_coordinates_airfoil, color='orange', label='Airfoil')

    plt.xlim(0, 1)  # Límites en el eje x desde 0 hasta 6
    plt.ylim(-0.1, 0.1)  # Límites en el eje y desde 0 hasta 10

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Camber')

    plt.legend()

    plt.show()

#-----------------------------------------------------------------#

# PRUEBAS

""" df = pd.read_csv(Datos.archivo_csv)

camber_m = camber_med(df)

print('Curvatura máxima:', camber_m) """

