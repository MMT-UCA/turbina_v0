#-----------------------------------------------------------------#
#MÓDULO PRINCIPAL - AVIÓN
#-----------------------------------------------------------------#
#IMPORTS

from Datos import Datos
import matplotlib.pyplot as plt
import numpy as np
import Helice_Module
import csv
import pandas as pd
import os
import Load_Module

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

#CSV principal

def csv_principal():

    perfil_variable = Datos.perfil_variable
    if perfil_variable == True:
        df_csv_variable = pd.read_csv(Datos.archivo_csv_variable)
        load_Re_map = Load_Module.load_Re(df_csv_variable)

    carpeta_resultados = os.path.join(os.getcwd(), 'Archivos_Resultados')
    if not os.path.exists(carpeta_resultados):
        os.makedirs(carpeta_resultados)

    def crear_csv_principal(datos, nombre_archivo):

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            encabezados = ['t', 'x', 'C', 'a', 'Fd', 'T', 'W']
            escritor_csv.writerow(encabezados)

            for fila in datos:
                escritor_csv.writerow([fila[key] for key in encabezados])

    datos_principal = principal(Datos.Beta)

    nombre_archivo = 'resultados_principal_cuerdatorsion_var.csv'
    crear_csv_principal(datos_principal, nombre_archivo)
    print(f"Se ha creado el archivo CSV '{nombre_archivo}'.")

#-----------------------------------------------------------------#

#PLOT

def plot_complete_aircraft():

    carpeta_plots = os.path.join(os.getcwd(), 'Archivos_Resultados', 'Plots')
    if not os.path.exists(carpeta_plots):
        os.makedirs(carpeta_plots)

    def plot_T_Fd_C_csv():

        df = pd.read_csv(Datos.resultados_principal_csv)
        t = df['t']
        T = df['T']
        Fd = df['Fd']
        C = df['C']

        fig, ax1 = plt.subplots(figsize=(9, 6))

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

        ruta_archivo = os.path.join(carpeta_plots, 'T_Fd_C.png')
        plt.savefig(ruta_archivo)

        print(f"Se ha creado la imagen T_Fd_C.png.")

    def plot_W_a_csv():

        df = pd.read_csv(Datos.resultados_principal_csv)
        t = df['t']
        W = df['W']
        a = df['a']

        fig, ax1 = plt.subplots(figsize=(9, 6))

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

        ruta_archivo = os.path.join(carpeta_plots, 'W_a.png')
        plt.savefig(ruta_archivo)

        print(f"Se ha creado la imagen W_a.png.")

    plot_W_a_csv()
    plot_T_Fd_C_csv()