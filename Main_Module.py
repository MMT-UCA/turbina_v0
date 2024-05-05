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

def avion(C,Z,Cd,T,x):

    T = Datos.n_motor*T
    C_1 = C
    error = 0
    j = 0
    while abs(error) > 0.01 or j < 150:
        C_anterior = C_1
        Fd = 0.5 * Helice_Module.rho(Z) * Cd * Datos.A_a * (C_1 ** 2)
        C_1 = C + (T - Fd) / (Datos.m * Datos.dt)
        error = C_1 - C_anterior
        j += 1 

    x_1 = x + C * Datos.dt + (T - Fd) / (Datos.m * (Datos.dt ** 2))
    a = (T - Fd) / Datos.m

    return x_1, a, C_1, Fd

#-----------------------------------------------------------------#

def principal(Beta):

    lim_error = 0.1
    T_anterior = 0
    T = 0
    C_dt = 0
    Z = Datos.Z
    C = Datos.C
    Cd = Datos.C_d
    t_fin = Datos.t_fin
    dt = Datos.dt
    x = Datos.x
    lista:list[map] = []

    for t in range(0, t_fin + dt, dt):
        
        j = 0
        error_T = 1
        while abs(error_T) > lim_error and j < 150:
            T_anterior = T
            C_media = 0.5 * C + 0.5 * C_dt
            T, Q, W = Helice_Module.helice(C,Beta)
            x_dt, a, C_dt, Fd = avion(C,Z,Cd,T,x)
            error_T = T - T_anterior
            j += 1 
        C = C_dt
        x = x_dt
        lista.append({'t': t,'x': x,'C': C, 'a': a, 'Fd': Fd, 'T': T, 'W': W})

    return lista
#-----------------------------------------------------------------#

def acel_maxima():

    Beta = 0
    delta_Beta = 0.1
    lim_error = 0.1
    t_fin = Datos.t_fin_acel
    dt = Datos.dt_acel
    Cd = Datos.C_d
    Z = Datos.Z
    x = Datos.x
    C = 0
    C_dt = 0
    Beta_optimo_seed = 26
    Beta_optimo = Beta_optimo_seed
    lista_acel:list[map] = []

    for t in range(0, t_fin + dt, dt):
        print('t:', t)

        T = 1
        T_anterior = 0

        #
        Beta = Beta_optimo
        j = 0
        while not T_anterior >= T or j > 100: #Aceleración máxima
            T_anterior = T
            C_media = 0.5 * C + 0.5 * C_dt
            T, Q, W = Helice_Module.helice(C,Beta)
            x_dt, a, C_dt, Fd = avion(C,Z,Cd,T,x)
            Beta = Beta + delta_Beta
            #print('Beta, T_anterior, T:', Beta, T_anterior, T)
            j += 1
        #

        Beta_optimo = Beta - 2*delta_Beta
        i = 0
        T = 1
        T_anterior = 0
        while not T_anterior >= T or i > 100: #Beta óptimo
            T_anterior = T
            C_media = 0.5 * C + 0.5 * C_dt
            T, Q, W = Helice_Module.helice(C,Beta_optimo)
            x_dt, a, C_dt, Fd = avion(C,Z,Cd,T,x)
            #print('Beta_optimo, T_anterior, T:', Beta_optimo, T_anterior, T)
            i += 1

        C = C_dt
        x = x_dt
        eta = C * T/W/2

        lista_acel.append({'t': t,'Beta_opt': Beta_optimo,'x': x,'C': C, 'a': a, 'Fd': Fd, 'T': T, 'W': W, 'eta': eta})

    return lista_acel

#-----------------------------------------------------------------#
#PRUEBAS

""" listaa = acel_maxima()

listaa1 = listaa[0]
listaa2 = listaa[1]
listaa4 = listaa[2]
listaa3 = listaa[6]

print('posición 0:', listaa1)
print('posición 1:', listaa2)
print('posición 2:', listaa4)
print('posición 6:', listaa3) """

""" Beta = Beta_optimo
        j = 0
        while T2 < T3 and T2 < T1 and j < 100: #Aceleración máxima
            T1 = T2
            T2 = T3
            i = 0
            T = 0
            error_T = 1
            while abs(error_T) > lim_error and j < 150:
                T_anterior = T
                C_media = 0.5 * C + 0.5 * C_dt
                T, Q, W = Helice_Module.helice(C,Beta)
                x_dt, a, C_dt, Fd = avion(C,Z,Cd,T,x)
                error_T = T - T_anterior
                i += 1 
            Beta = Beta + delta_Beta
            T3 = T
            j += 1 """

#-----------------------------------------------------------------#
#CSV principal

#def csv_principal():

#-----------------------------------------------------------------#
#PLOT Acel_maxima T, Fd, W
def plot_amax_T_Fd_W():

    listaa = acel_maxima()

    t = [diccionario['t'] for diccionario in listaa]

    T = [diccionario['T'] for diccionario in listaa]

    Fd = [diccionario['Fd'] for diccionario in listaa]

    W = [diccionario['W'] for diccionario in listaa]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('W', color='black')
    ax1.plot(t, W, color='green', linestyle='--', label='W')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.set_ylabel('T y Fd', color='black')
    ax2.plot(t, T, color='blue', linestyle='--', label='T')
    ax2.plot(t, Fd, color='red', linestyle='-.', label='Fd')
    ax2.tick_params(axis='y', labelcolor='black')

    plt.title('T, Fd, W')

    fig.legend(loc="upper right")

    fig.tight_layout()

    plt.show()



#-----------------------------------------------------------------#
#PLOT Fd, T, C

def plot_T_Fd_C():

    lista_plot = principal(Datos.Beta)

    t = [diccionario['t'] for diccionario in lista_plot]

    T = [diccionario['T'] for diccionario in lista_plot]

    Fd = [diccionario['Fd'] for diccionario in lista_plot]

    C = [diccionario['C'] for diccionario in lista_plot]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('T y Fd', color='black')
    ax1.plot(t, T, color='green', linestyle='--', label='T')
    ax1.plot(t, Fd, color='red', linestyle='-.', label='Fd')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.set_ylabel('C', color='black')
    ax2.plot(t, C, color='blue', linestyle='--', label='C')
    ax2.tick_params(axis='y', labelcolor='black')

    plt.title('T, Fd, C')

    fig.legend(loc="upper right")

    fig.tight_layout()

    plt.show()

#-----------------------------------------------------------------#
#PLOT W, a

def plot_T_Fd_C():

    lista_plot = principal(Datos.Beta)

    t = [diccionario['t'] for diccionario in lista_plot]

    W = [diccionario['W'] for diccionario in lista_plot]

    a = [diccionario['a'] for diccionario in lista_plot]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('W', color='black')
    ax1.plot(t, W, color='red', linestyle='--', label='W')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.set_ylabel('a', color='black')
    ax2.plot(t, a, color='blue', linestyle='--', label='a')
    ax2.tick_params(axis='y', labelcolor='black')

    plt.title('W, a')

    fig.legend(loc="upper right")

    fig.tight_layout()

    plt.show()





