#-----------------------------------------------------------------#
#Inacabado
#IMPORTS

import math
import pandas as pd
import matplotlib.pyplot as plt
import Datos
import Main_Module
import CoolProp.CoolProp as CP
import Interpolate_Extrapolate_Module

#-----------------------------------------------------------------#

#LLAMA_HÉLICE

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# Lee los datos desde el archivo CSV (carga_Cl_Cd)
df_1 = pd.read_csv(Datos.url_Re50000, skiprows=10)
df_2 = pd.read_csv(Datos.url_Re100000, skiprows=10)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#Torsión

def Torsion():

    alfa_rad = Datos.alfa_diseno * (Datos.pi / 180) #radianes
    n = Datos.RPM / 60 #rps

    j = Datos.C_crucero / (n * Datos.D)

    #Beta variable con el radio (torsión)

    Beta_crucero = [] # Definir Beta_crucero como una lista vacía

    r = Datos.r_o
    while r <= (Datos.D)/2:
        valor = (math.atan(Datos.D * j / (2 * math.pi * r)) + alfa_rad) * (180 / math.pi)
        Beta_crucero.append(valor)
        r += Datos.dr

    Beta_n_crucero = (math.atan(Datos.D * j / (2 * Datos.pi * 3 * Datos.D / 8)) + alfa_rad) * 180 / Datos.pi
    return Beta_crucero, Beta_n_crucero


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#Velocidades inducidas
def velocidades_inducidas(r,T_anterior,Beta_rad,C):
    rhoz = Main_Module.rho(Datos.Z)
    m = Datos.m_vind
    a = Datos.a_vind
    n = Datos.n_vind
    r_max = Datos.D / 2

    r_n = (r - Datos.r_o) / (r_max - Datos.r_o)
    f_x = ((2.64 * T_anterior) / (r_max - Datos.r_o)) * ((r_n) ** (m)) * ((1 - ((r_n) / a)) ** (n))

    if f_x < 0:
        f_x = 0

    #Ratio P/D variable
    ratio_PD = (r / r_max) * Datos.pi * math.tan(Beta_rad * Datos.pi / 180)
    f_theta = (f_x / Datos.pi) * (ratio_PD / (r / r_max))
    C_i = (((C ^ 2) / 4) + (f_x / (4 * rhoz * Datos.pi * r))) ** (0.5) - (C / 2)

    if C_i > 340:
        C_i = 340
    
    if abs(C_i + C) < 1E-05 or f_theta < 0:
        omega_i = 0
    else:
        V_i = f_theta / (2 * Datos.pi * r * rhoz * (C + C_i))
        if V_i > 340:
            V_i = 340
        omega_i = V_i / r

    return C_i, omega_i

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#HÉLICE

def helice(C):

    rhoz = Main_Module.rho(Datos.Z)
    Tempe = Main_Module.Temp(Datos.Z)
    Presi = Main_Module.Pres(Datos.Z) * 1000
    Visc = CP.PropsSI("V", "T", Tempe, "P", Presi, "air")
    Beta_crucero, Beta_n_crucero = Torsion()
    T = 0
    T_anterior = 1 

    j = 0
    #Bucle
    while abs(T - T_anterior) >= 0.01 and j <= 200:
        T_anterior = T
        T = 0
        Q = 0
        i = 0
        r_vind = Datos.r_o
        while r_vind <= (Datos.D)/2:
            Beta_radio = Datos.Beta - Beta_n_crucero + Beta_crucero[i]
            Beta_rad = Beta_radio * Datos.pi / 180
            #Call velocidades inducidas 
            Ci, omega_i = velocidades_inducidas(r_vind, T_anterior,Beta_rad,C)
            C_Tcuad = (C + Ci) ** 2 + ((Datos.omega - omega_i) * r_vind) ** 2
            Phi_rad = math.atan((C + Ci) / ((Datos.omega - omega_i) * r_vind))
        
            #Cálculo de beta en cada posición
            alfa_rad = Beta_rad - Phi_rad
            Phi_grad = Phi_rad * 180 / Datos.pi
            alfa = 180 * alfa_rad / Datos.pi
            Re = rhoz * (C_Tcuad) ** 0.5 * Datos.cuerda / Visc
            #####Call Cl_Cd#####
            Cl, Cd = Interpolate_Extrapolate_Module.Interpolate_Extrapolate(alfa, Re)

            #Cálculo de Mach
            A_sonido = CP.PropsSI("A", "T", Tempe, "P", Presi, "air")
            Mach = ((C_Tcuad) ** 0.5) / A_sonido
            #####Call Cl_Cd corregido#####
            Cl_corregido, Cd_corregido = Interpolate_Extrapolate_Module.Cl_Cd_corregido(alfa,Cl,Cd,Mach)

            #Cálculo de tracción y potencia
            dTrac = C_Tcuad * (Cl_corregido * math.cos(Phi_rad) - Cd_corregido * math.sin(Phi_rad)) * Datos.dr
            dQ = C_Tcuad * (Cl_corregido * math.sin(Phi_rad) + Cd_corregido * math.cos(Phi_rad)) * r_vind * Datos.dr
            T = T + dTrac
            Q = Q + dQ

            i += 1
            r_vind += Datos.dr
        T = Datos.Palas * 0.5 * Datos.cuerda * rhoz * T
        Q = Datos.Palas * 0.5 * Datos.cuerda * rhoz * Q
        j += 1 
    if j >= 200:
        T = 0
        Q = 0

    W = Q * Datos.omega

    return W, T, Q

#-----------------------------------------------------------------#
#PRUEBAS

W, T, Q = helice(0)

print('W,T,Q:', W, T, Q)

#Beta_crucero = Torsion()    
#print(Beta_crucero)    
#print(Beta_n_crucero)

#pres_resultante = Main_Module.Pres(Datos.Z)
#pres_resultante_pas = Presi


#print(f"Altitud: {Datos.Z} metros")
#print(f"Presión: {pres_resultante} kPa") 
#print(f"Presión_Pascales: {pres_resultante_pas} Pa") 
#print(f"Viscosidad: {Visc} ") 
#print(f"A_sonido: {Beta_crucero} ") 