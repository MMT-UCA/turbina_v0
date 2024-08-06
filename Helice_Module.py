#-----------------------------------------------------------------#
#MÓDULO HÉLICE
#Cálculos de Tracción, Potencia, Rendimiento propulsivo
#-----------------------------------------------------------------#
#IMPORTS

import math
import pandas as pd
import matplotlib.pyplot as plt
from Datos import Datos
import CoolProp.CoolProp as CP
import Interpolate_Extrapolate_Module
import csv
import numpy as np
import Chord_Twist_Module
import Airfoil_Module
import Load_Module
import os

#-----------------------------------------------------------------#
#FUNCIONES
#Función cálculo Temperatura
def Temp(Z) :
    if Z < 11000 :
        return 288.19 - 0.00649*Z
    elif Z < 25000 :
        return 216.69
    else :
        return 141.94 + 0.00299*Z
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#Función cálculo Presión
def Pres(Z) :
    if Z < 11000 :
        return 101.29 * (Temp(Z) / 288.08) ** 5.256
    elif Z < 25000 :
        return 22.65 * math.exp(1.73 - 0.000157 * Z)
    else :
        return 2.488 * (Temp(Z) / 216.6) ** -11.388
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#Función cálculo Densidad
def rho(Z) :
    return Pres(Z)/(0.287*Temp(Z))

#-----------------------------------------------------------------#

#Velocidades inducidas
def velocidades_inducidas(r,T_anterior,Beta_rad,C):
    rhoz = rho(Datos.Z)
    m = Datos.m_vind
    a = Datos.a_vind
    n = Datos.n_vind
    r_max = Datos.D / 2

    r_n = (r - Datos.r_o) / (r_max - Datos.r_o)
    f_x = ((2.64 * T_anterior) / (r_max - Datos.r_o)) * ((r_n) ** (m)) * ((1 - ((r_n) / a)) ** (n))

    if f_x < 0:
        f_x = 0

    #Ratio P/D variable
    ratio_PD = (r / r_max) * math.pi * math.tan(Beta_rad * math.pi / 180)
    f_theta = (f_x / math.pi) * (ratio_PD / (r / r_max))
    C_i = (((C ** 2) / 4) + (f_x / (4 * rhoz * math.pi * r))) ** (0.5) - (C / 2)

    if C_i > 340:
        C_i = 340
    
    if abs(C_i + C) < 1E-05 or f_theta < 0:
        omega_i = 0
    else:
        V_i = f_theta / (2 * math.pi * r * rhoz * (C + C_i))
        if V_i > 340:
            V_i = 340
        omega_i = V_i / r

    return C_i, omega_i

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#HÉLICE

def helice(C,Beta):
    
    rhoz = rho(Datos.Z)
    Tempe = Temp(Datos.Z)
    Presi = Pres(Datos.Z) * 1000
    Visc = CP.PropsSI("V", "T", Tempe, "P", Presi, "air")
    Beta_crucero, Beta_n_crucero = Chord_Twist_Module.Torsion()
    valor_cuerda, valor_cuerda_media = Chord_Twist_Module.cuerda()
    T = 0
    T_anterior = 1 
    perfil_variable = Datos.perfil_variable
    if perfil_variable == True:
        df_csv_variable = pd.read_csv(Datos.archivo_csv_variable)
    else:
        df_csv_variable = None
        


    j = 0
    #Bucle
    while abs(T - T_anterior) >= 0.01 and j <= 200:
        T_anterior = T
        T = 0
        Q = 0
        i = 0
        r_vind = Datos.r_o
        while r_vind <= (Datos.D)/2:
            df_airfoil = Airfoil_Module.coordenadas_perfil(r_vind,perfil_variable)
            Beta_radio = Beta - Beta_n_crucero + Beta_crucero[i]
            Beta_rad = Beta_radio * math.pi / 180
            #Call velocidades inducidas 
            Ci, omega_i = velocidades_inducidas(r_vind, T_anterior,Beta_rad,C)
            C_Tcuad = (C + Ci) ** 2 + ((Datos.omega - omega_i) * r_vind) ** 2
            Phi_rad = math.atan((C + Ci) / ((Datos.omega - omega_i) * r_vind))
        
            #Cálculo de beta en cada posición
            alfa_rad = Beta_rad - Phi_rad
            Phi_grad = Phi_rad * 180 / math.pi
            alfa = 180 * alfa_rad / math.pi
            Re = rhoz * (C_Tcuad) ** 0.5 * valor_cuerda[i] / Visc
            #####Call Cl_Cd#####
            Cl, Cd = Interpolate_Extrapolate_Module.Interpolate_Extrapolate(alfa, Re,r_vind,perfil_variable,df_airfoil,df_csv_variable,j,C)

            #Cálculo de Mach
            A_sonido = CP.PropsSI("A", "T", Tempe, "P", Presi, "air")
            Mach = ((C_Tcuad) ** 0.5) / A_sonido
            #####Call Cl_Cd corregido#####
            Cl_corregido, Cd_corregido, transonico, supersonico = Interpolate_Extrapolate_Module.Cl_Cd_corregido(alfa,Cl,Cd,Mach,r_vind,perfil_variable,df_airfoil)
            #Cálculo de tracción y potencia
            dTrac = C_Tcuad * (Cl_corregido * math.cos(Phi_rad) - Cd_corregido * math.sin(Phi_rad)) * Datos.dr
            dQ = C_Tcuad * (Cl_corregido * math.sin(Phi_rad) + Cd_corregido * math.cos(Phi_rad)) * r_vind * Datos.dr
            T = T + dTrac
            Q = Q + dQ

            i += 1
            r_vind += Datos.dr
        T = Datos.Palas * 0.5 * valor_cuerda_media * rhoz * T
        Q = Datos.Palas * 0.5 * valor_cuerda_media * rhoz * Q
        j += 1 
    if j > 200:
        if abs(T - T_anterior) <=300:
            T = (T + T_anterior)/2
            Q = Q
        else:
            T = 0
            Q = 0
    

    if T < 0:
        T = 0
        Q = 0

    W = Q * Datos.omega

    return  T, Q, W

#-----------------------------------------------------------------#
#CSV
#Crea archivos csv de: T-C, W-C, eta-C, Ct-J, Cp-J

def csv_complete(betas):

    perfil_variable = Datos.perfil_variable
    if perfil_variable == True:
        df_csv_variable = pd.read_csv(Datos.archivo_csv_variable)
        load_Re_map = Load_Module.load_Re(df_csv_variable)

    carpeta_resultados = os.path.join(os.getcwd(), 'Archivos_Resultados')
    if not os.path.exists(carpeta_resultados):
        os.makedirs(carpeta_resultados)

    #T vs C
    def crear_csv(datos, nombre_archivo):

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            encabezados = ['C', 'T(B=10°)', 'T(B=20°)', 'T(B=30°)', 'T(B=40°)', 'T(B=50°)', 'T(B=60°)', 'T(B=70°)', 'T(B=80°)']
            escritor_csv.writerow(encabezados)

            for C, valores in datos.items():
                fila = [C]
                for valor in valores:
                    fila.append(valor)
                escritor_csv.writerow(fila)
    
    #W vs C
    def crear_csv_W(datos, nombre_archivo):

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            encabezados = ['C', 'W(B=10°)', 'W(B=20°)', 'W(B=30°)', 'W(B=40°)', 'W(B=50°)', 'W(B=60°)', 'W(B=70°)', 'W(B=80°)']
            escritor_csv.writerow(encabezados)

            for C, valores in datos.items():
                fila = [C]
                for valor in valores:
                    fila.append(valor)
                escritor_csv.writerow(fila)
    
    #Eta vs C
    def crear_csv_eta(datos, nombre_archivo):

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            encabezados = ['C', 'eta(B=10°)', 'eta(B=20°)', 'eta(B=30°)', 'eta(B=40°)', 'eta(B=50°)', 'eta(B=60°)', 'eta(B=70°)', 'eta(B=80°)']
            escritor_csv.writerow(encabezados)

            for C, valores in datos.items():
                fila = [C]
                for valor in valores:
                    fila.append(valor)
                escritor_csv.writerow(fila)
    
    #Ct vs J
    def crear_csv_Ct(datos, nombre_archivo):

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            encabezados = ['J', 'Ct(B=10°)', 'Ct(B=20°)', 'Ct(B=30°)', 'Ct(B=40°)', 'Ct(B=50°)', 'Ct(B=60°)', 'Ct(B=70°)', 'Ct(B=80°)']
            escritor_csv.writerow(encabezados)

            for J, valores in datos.items():
                fila = [J]
                for valor in valores:
                    fila.append(valor)
                escritor_csv.writerow(fila)
    
    #Cp vs J
    def crear_csv_Cp(datos, nombre_archivo):

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            encabezados = ['J', 'Cp(B=10°)', 'Cp(B=20°)', 'Cp(B=30°)', 'Cp(B=40°)', 'Cp(B=50°)', 'Cp(B=60°)', 'Cp(B=70°)', 'Cp(B=80°)']
            escritor_csv.writerow(encabezados)

            for J, valores in datos.items():
                fila = [J]
                for valor in valores:
                    fila.append(valor)
                escritor_csv.writerow(fila)


    datos_T:map = {}
    datos_W:map = {}
    datos_eta:map = {}
    datos_Ct:map = {}
    datos_Cp:map = {}

    for Beta in betas:
        values_T:list = []
        values_W:list = []
        values_eta:list = []
        values_Ct:list = []
        values_Cp:list = []
        T_ant = 1
        for C in range(0,401):
            J = C/(Datos.RPS * Datos.D)
            if T_ant != 0:
                T, Q, W = helice(C, Beta)
                print(C,Beta,T)
                T_ant = T
            else:
                T = 0
                W = 0
            rhoz = rho(Datos.Z)
            Ct = T/(rhoz*((Datos.RPS)**2)*((Datos.D)**4))
            Cp = W/(rhoz*((Datos.RPS)**3)*((Datos.D)**5))
            if Ct == 0:
                eta = 0
            else:
                eta = (Ct*J)/Cp
            values_T.append([C, T])
            values_W.append([C, W])
            values_Ct.append([J,Ct])
            values_Cp.append([J,Cp])
            values_eta.append([C,eta])
            if C not in datos_T:
                datos_T[C] = [T]
            else:
                datos_T[C].append(T)
            if C not in datos_W:
                datos_W[C] = [W]
            else:
                datos_W[C].append(W)
            if J not in datos_Ct:
                datos_Ct[J] = [Ct]
            else:
                datos_Ct[J].append(Ct)
            if J not in datos_Cp:
                datos_Cp[J] = [Cp]
            else:
                datos_Cp[J].append(Cp)
            if C not in datos_eta:
                datos_eta[C] = [eta]
            else:
                datos_eta[C].append(eta)


    nombre_archivo_T = 'Archivos_Resultados/T_C.csv'
    crear_csv(datos_T, nombre_archivo_T)
    print(f"Se ha creado el archivo CSV '{nombre_archivo_T}' en la carpeta 'Archivos_Resultados'.")
    nombre_archivo_W = 'Archivos_Resultados/W_C.csv'
    crear_csv_W(datos_W, nombre_archivo_W)
    print(f"Se ha creado el archivo CSV '{nombre_archivo_W}' en la carpeta 'Archivos_Resultados'.")
    nombre_archivo_eta = 'Archivos_Resultados/eta_C.csv'
    crear_csv_eta(datos_eta, nombre_archivo_eta)
    print(f"Se ha creado el archivo CSV '{nombre_archivo_eta}' en la carpeta 'Archivos_Resultados'.")
    nombre_archivo_Ct = 'Archivos_Resultados/Ct_J.csv'
    crear_csv_Ct(datos_Ct, nombre_archivo_Ct)
    print(f"Se ha creado el archivo CSV '{nombre_archivo_Ct}' en la carpeta 'Archivos_Resultados'.")
    nombre_archivo_Cp = 'Archivos_Resultados/Cp_J.csv'
    crear_csv_Cp(datos_Cp, nombre_archivo_Cp)
    print(f"Se ha creado el archivo CSV '{nombre_archivo_Cp}' en la carpeta 'Archivos_Resultados'.")

#-----------------------------------------------------------------#

#PLOT
def plot_complete(betas):

    carpeta_plots = os.path.join(os.getcwd(), 'Archivos_Resultados', 'Plots')
    if not os.path.exists(carpeta_plots):
        os.makedirs(carpeta_plots)

    def plot_T_C():

        df = pd.read_csv(Datos.T_C_csv)
        valores_C = df['C']

        colores = ['cyan', 'red', 'green', 'blue', 'yellow', 'magenta', 'brown', 'pink']

        i = 1
        plt.figure(figsize=(10, 7))
        for Beta, color in zip(betas, colores):
            columna_T = f"T(B={Beta}°)"
            valores_T = df[columna_T]
            plt.plot(valores_C, valores_T,label=f'Beta = {Beta}°', color=color)

        plt.xlabel('C [m/s]')
        plt.ylabel('T [N]')
        plt.title('T vs C')

        plt.legend()

        ruta_archivo = os.path.join(carpeta_plots, 'T_vs_C.png')
        plt.savefig(ruta_archivo)

        print(f"Se ha creado la imagen T_vs_C.png.")


    def plot_W_C():

        df = pd.read_csv(Datos.W_C_csv)
        valores_C = df['C']

        colores = ['cyan', 'red', 'green', 'blue', 'yellow', 'magenta', 'brown', 'pink']

        i = 1
        plt.figure(figsize=(10, 7))
        for Beta, color in zip(betas, colores):
            columna_W = f"W(B={Beta}°)"
            valores_W = df[columna_W]
            plt.plot(valores_C, valores_W,label=f'Beta = {Beta}°', color=color)

        plt.xlabel('C [m/s]')
        plt.ylabel('W [W]')
        plt.title('W vs C')

        plt.legend()

        ruta_archivo = os.path.join(carpeta_plots, 'W_vs_C.png')
        plt.savefig(ruta_archivo)

        print(f"Se ha creado la imagen W_vs_C.png.")


    def plot_eta_C():

        df = pd.read_csv(Datos.eta_C_csv)
        valores_C = df['C']

        colores = ['cyan', 'red', 'green', 'blue', 'yellow', 'magenta', 'brown', 'pink']

        i = 1
        plt.figure(figsize=(10, 7))
        for Beta, color in zip(betas, colores):
            columna_eta = f"eta(B={Beta}°)"
            valores_eta = df[columna_eta]
            plt.plot(valores_C, valores_eta,label=f'Beta = {Beta}°', color=color)

        plt.xlabel('C [m/s]')
        plt.ylabel('eta')
        plt.title('eta vs C')

        plt.legend()

        ruta_archivo = os.path.join(carpeta_plots, 'eta_vs_C.png')
        plt.savefig(ruta_archivo)

        print(f"Se ha creado la imagen eta_vs_C.png.")


    plot_T_C()
    plot_W_C()
    plot_eta_C()

#-----------------------------------------------------------------#


