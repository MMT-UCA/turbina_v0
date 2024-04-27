#-----------------------------------------------------------------#
#INACABADO
#IMPORTS

import math
import Datos
import matplotlib.pyplot as plt
import numpy as np
import Helice_Module
import Interpolate_Extrapolate_Module

#-----------------------------------------------------------------#

def avion(C,Z,Cd,T):

    T = Datos.n_motor*T
    C_1 = C
    error = 0
    j = 0
    while abs(error) > 0.01 or j < 150:
        C_anterior = C_1
        Fd = 0.5 * Helice_Module.rho(Z) * Cd * Datos.A_a * (C_1 ** 2)
        C_1 = C + (T - Fd) / Datos.m * Datos.dt
        error = C_1 - C_anterior
        j += 1 

    x_1 = Datos.x + C * Datos.dt + (T - Fd) / Datos.m * (Datos.dt ** 2)
    a = (T - Fd) / Datos.m

    return x_1, a, C_1

#-----------------------------------------------------------------#

def principal(Beta):

    lim_error = 0.1
    T_anterior = 0
    T = 0
    C_dt = 0
    Z = Datos.Z
    C = Datos.C
    t_fin = Datos.t_fin
    dt = Datos.dt
    lista:list[map] = []

    for t in range(0, t_fin + dt, dt):
        
        j = 0
        error_T = 1
        while abs(error_T) > lim_error and j < 150:
            T_anterior = T
            C_media = 0.5 * C + 0.5 * C_dt
            T, Q, W = Helice_Module.helice(C,Beta)
            Cd = Datos.C_d
            x_dt, a, C_dt = avion(C,Z,Cd,T)
            error_T = T - T_anterior
            j += 1 
        C = C_dt
        x = x_dt
        lista.append({'t': t,'C': C, 'x': x})

    return lista
#-----------------------------------------------------------------#
#PRUEBAS
""" C = 0
Beta = 60

T, Q, W = Helice_Module.helice(C,Beta)

x_1, a, C_1 = avion(C,Datos.Z,Datos.C_d,T)

print('x_1,a,C_1:',x_1, a, C_1) """

listaa = principal(60)

listaa1 = listaa[0]
listaa2 = listaa[1]
listaa3 = listaa[6]

print('posición 0:', listaa1)
print('posición 1:', listaa2)
print('posición 6:', listaa3)