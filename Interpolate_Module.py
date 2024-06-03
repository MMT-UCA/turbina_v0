#-----------------------------------------------------------------#
#MÓDULO DE INTERPOLACIÓN 
#-----------------------------------------------------------------#
#IMPORTS

import pandas as pd
import matplotlib.pyplot as plt
import Datos
import Airfoil_Module

#-----------------------------------------------------------------#

def interpolate_fcn(x_1,y_1,x_2,y_2,x_3):

    if x_1 == x_2:
        y_3 = y_1
    else:
        y_3 = y_1 + ((y_2-y_1)/(x_2-x_1))*(x_3-x_1)

    return y_3

#-----------------------------------------------------------------#
#Devuelve los límites del intervalo en el que se encuentra alpha
def interpolate_alpha(x_list, y_list, alpha):
    # Encontrar el valor inmediatamente superior en la lista
    alpha_upper = x_list[x_list >= alpha].min()

    # Encontrar el valor inmediatamente inferior en la lista
    alpha_lower = x_list[x_list <= alpha].max()
    
    # Obtener los valores de Cl correspondientes a los alphas encontrados
    Cl_lower = y_list[x_list == alpha_lower].iloc[0] if not pd.isnull(alpha_lower) else None
    Cl_upper = y_list[x_list == alpha_upper].iloc[0] if not pd.isnull(alpha_upper) else None
            
    return (alpha_lower, Cl_lower), (alpha_upper, Cl_upper)

#-----------------------------------------------------------------#
#Funciones principales de interpolación de Cl y Cd en función de Re
def interpolate_Cl(alpha,Re,r,perfil_variable):

    if 50000 <= Re < 100000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,50000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,100000)
        Re_lower = 50000
        Re_upper = 100000
    elif 100000 <= Re < 200000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,100000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,200000)
        Re_lower = 100000
        Re_upper = 200000
    elif 200000 <= Re < 500000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,200000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,500000)
        Re_lower = 200000
        Re_upper = 500000
    elif 500000 <= Re < 1000000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,500000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,1000000)
        Re_lower = 500000
        Re_upper = 1000000
    elif Re == 1000000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,1000000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,1000000)
        Re_lower = 1000000
        Re_upper = 1000000
    else:
        # Si ninguna de las condiciones anteriores se cumple
        print("Re no está en ninguno de los rangos especificados")

    x_list = df['Alpha']
    y_list = df['Cl']
    lower_values, upper_values = interpolate_alpha(x_list, y_list, alpha)
    x_1, y_1 = lower_values
    x_2, y_2 = upper_values
    if alpha == x_1:
        Cl_lower = y_1
    if alpha == x_2:
        Cl_lower = y_2
    else:
        Cl_lower = interpolate_fcn(x_1,y_1,x_2,y_2,alpha)
    x_list_2 = df_2['Alpha']
    y_list_2 = df_2['Cl']
    lower_values_2, upper_values_2 = interpolate_alpha(x_list_2, y_list_2, alpha)
    x_1_2, y_1_2 = lower_values_2
    x_2_2, y_2_2 = upper_values_2
    if alpha == x_1_2:
        Cl_upper = y_1_2
    if alpha == x_2_2:
        Cl_upper = y_2_2
    else: 
        Cl_upper = interpolate_fcn(x_1_2,y_1_2,x_2_2,y_2_2,alpha)
    Cl_final = interpolate_fcn(Re_lower,Cl_lower,Re_upper,Cl_upper,Re)

    return Cl_final

def interpolate_Cd(alpha,Re,r,perfil_variable):

    if 50000 <= Re < 100000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,50000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,100000)
        Re_lower = 50000
        Re_upper = 100000
    elif 100000 <= Re < 200000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,100000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,200000)
        Re_lower = 100000
        Re_upper = 200000
    elif 200000 <= Re < 500000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,200000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,500000)
        Re_lower = 200000
        Re_upper = 500000
    elif 500000 <= Re < 1000000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,500000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,1000000)
        Re_lower = 500000
        Re_upper = 1000000
    elif Re == 1000000:
        df = Airfoil_Module.archivo_Re(r,perfil_variable,1000000)
        df_2 = Airfoil_Module.archivo_Re(r,perfil_variable,1000000)
        Re_lower = 1000000
        Re_upper = 1000000
    else:
        # Si ninguna de las condiciones anteriores se cumple
        print("Re no está en ninguno de los rangos especificados")

    x_list = df['Alpha']
    y_list = df['Cd']
    lower_values, upper_values = interpolate_alpha(x_list, y_list, alpha)
    x_1, y_1 = lower_values
    x_2, y_2 = upper_values
    if alpha == x_1:
        Cd_lower = y_1
    if alpha == x_2:
        Cd_lower = y_2
    else:
        Cd_lower = interpolate_fcn(x_1,y_1,x_2,y_2,alpha)
    x_list_2 = df_2['Alpha']
    y_list_2 = df_2['Cd']
    lower_values_2, upper_values_2 = interpolate_alpha(x_list_2, y_list_2, alpha)
    x_1_2, y_1_2 = lower_values_2
    x_2_2, y_2_2 = upper_values_2
    if alpha == x_1_2:
        Cd_upper = y_1_2
    if alpha == x_2_2:
        Cd_upper = y_2_2
    else: 
        Cd_upper = interpolate_fcn(x_1_2,y_1_2,x_2_2,y_2_2,alpha)
    Cd_final = interpolate_fcn(Re_lower,Cd_lower,Re_upper,Cd_upper,Re)

    return Cd_final


#PRUEBAS

#df = pd.read_csv(Datos.url_Re50000, skiprows=10)
#x_list = df['Alpha']
#y_list = df['Cl']
#alpha = 6.976800047586
#lower_values, upper_values = interpolate_alpha(x_list, y_list, alpha)
#print("Valor inferior de alpha y Cl:", lower_values)
#print("Valor superior de alpha y Cl:", upper_values)
#x_1, y_1 = lower_values
#x_2, y_2 = upper_values
#Cl_lower = interpolate_fcn(x_1,y_1,x_2,y_2,alpha)
#print("Valor de Cl lower:", Cl_lower)
#Re = 58000
#Cl = interpolate(alpha,Re)
#print("Valor de Cl:", Cl)

