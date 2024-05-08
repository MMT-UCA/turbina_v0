#-----------------------------------------------------------------#
#MÓDULO PRINCIPAL DE INTERPOLACIÓN Y EXTRAPOLACIÓN
#-----------------------------------------------------------------#
#IMPORTS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Extrapolate_Module
import Interpolate_Module
import Datos
import Camber_Module
import Factor_Corrector_Module

#-----------------------------------------------------------------#
#Función que calcula Cl y Cd para Re = [50000, 100000, 200000, 500000, 1000000]
def Interpolate_Extrapolate_Re(alpha,Re):
    # Re listado

    df_airfoil = pd.read_csv(Datos.archivo_csv)

    if Re == 50000:
        df = pd.read_csv(Datos.url_Re50000, skiprows=10)
    if Re == 100000:
        df = pd.read_csv(Datos.url_Re100000, skiprows=10)
    if Re == 200000:
        df = pd.read_csv(Datos.url_Re200000, skiprows=10)
    if Re == 500000:
        df = pd.read_csv(Datos.url_Re500000, skiprows=10)
    if Re == 1000000:
        df = pd.read_csv(Datos.url_Re1000000, skiprows=10)

    alpha_column = df['Alpha']
    alpha_min_tab = alpha_column.iloc[1]
    alpha_max_tab = alpha_column.iloc[-1]
    # Verificar si el alpha está presente en los datos de Cl y alpha para el Re dado
    if alpha in alpha_column.values:
        # Obtener el índice del valor de alpha en la columna
        idx = alpha_column[alpha_column == alpha].index[0]
        # Obtener el valor correspondiente de Cl
        Cl = df.loc[idx, 'Cl']
        Cd = df.loc[idx, 'Cd']
        return  Cl, Cd # Devolver el dato exacto
    if alpha_min_tab < alpha < alpha_max_tab:
        # Alpha dentro de los límites, realizar interpolación
        Cl = Interpolate_Module.interpolate_Cl(alpha,Re)
        Cd = Interpolate_Module.interpolate_Cd(alpha,Re)
        return Cl, Cd
    else:
        # Alpha fuera de los límites, realizar extrapolación
        simetria = Extrapolate_Module.symmetry(df_airfoil)
        if simetria == True:
            Cl, Cd = Extrapolate_Module.extrapolate_symmetrical(df,df_airfoil,alpha,Re)
        else:
            Cl, Cd = Extrapolate_Module.extrapolate_asymmetrical(df,df_airfoil,alpha,Re)
        return Cl, Cd
    


#-----------------------------------------------------------------#
#Función principal, calcula Cl y Cd para Re ≠ [50000, 100000, 200000, 500000, 1000000]
def Interpolate_Extrapolate(alpha,Re):

    df_airfoil = pd.read_csv(Datos.archivo_csv)

    if Re in [50000, 100000, 200000, 500000, 1000000]:
        Cl, Cd = Interpolate_Extrapolate_Re(alpha,Re)
    else: #Re ≠ [50000, 100000, 200000, 500000, 1000000]
        if 50000 < Re < 100000:
            Re_lower = 50000
            Re_upper = 100000
            Cl_lower, Cd_lower = Interpolate_Extrapolate_Re(alpha,Re_lower)
            Cl_upper, Cd_upper = Interpolate_Extrapolate_Re(alpha,Re_upper)
            Cl = Interpolate_Module.interpolate_fcn(Re_lower,Cl_lower,Re_upper,Cl_upper,Re)
            Cd = Interpolate_Module.interpolate_fcn(Re_lower,Cd_lower,Re_upper,Cd_upper,Re)
        if 100000 < Re < 200000:
            Re_lower = 100000
            Re_upper = 200000
            Cl_lower, Cd_lower = Interpolate_Extrapolate_Re(alpha,Re_lower)
            Cl_upper, Cd_upper = Interpolate_Extrapolate_Re(alpha,Re_upper)
            Cl = Interpolate_Module.interpolate_fcn(Re_lower,Cl_lower,Re_upper,Cl_upper,Re)
            Cd = Interpolate_Module.interpolate_fcn(Re_lower,Cd_lower,Re_upper,Cd_upper,Re)
        if 200000 < Re < 500000:
            Re_lower = 200000
            Re_upper = 500000
            Cl_lower, Cd_lower = Interpolate_Extrapolate_Re(alpha,Re_lower)
            Cl_upper, Cd_upper = Interpolate_Extrapolate_Re(alpha,Re_upper)
            Cl = Interpolate_Module.interpolate_fcn(Re_lower,Cl_lower,Re_upper,Cl_upper,Re)
            Cd = Interpolate_Module.interpolate_fcn(Re_lower,Cd_lower,Re_upper,Cd_upper,Re)
        if 500000 < Re < 1000000:
            Re_lower = 500000
            Re_upper = 1000000
            Cl_lower, Cd_lower = Interpolate_Extrapolate_Re(alpha,Re_lower)
            Cl_upper, Cd_upper = Interpolate_Extrapolate_Re(alpha,Re_upper)
            Cl = Interpolate_Module.interpolate_fcn(Re_lower,Cl_lower,Re_upper,Cl_upper,Re)
            Cd = Interpolate_Module.interpolate_fcn(Re_lower,Cd_lower,Re_upper,Cd_upper,Re)
        if 50000 > Re:
            df = pd.read_csv(Datos.url_Re50000, skiprows=10)
            alpha_column = df['Alpha']
            alpha_min_tab = alpha_column.iloc[1]
            alpha_max_tab = alpha_column.iloc[-1]
            simetria = Extrapolate_Module.symmetry(df_airfoil)
            if simetria == True:
                if alpha_min_tab < alpha < alpha_max_tab: 
                    Cl, Cd = Interpolate_Extrapolate_Re(alpha, 50000)
                else:
                    Cl, Cd = Extrapolate_Module.extrapolate_symmetrical(df,df_airfoil,alpha,Re)
            else:
                if alpha_min_tab < alpha < alpha_max_tab: 
                    Cl, Cd = Interpolate_Extrapolate_Re(alpha, 50000)
                else:
                    Cl, Cd = Extrapolate_Module.extrapolate_asymmetrical(df,df_airfoil,alpha,Re)
        if 1000000 < Re:
            df = pd.read_csv(Datos.url_Re1000000, skiprows=10)
            alpha_column = df['Alpha']
            alpha_min_tab = alpha_column.iloc[1]
            alpha_max_tab = alpha_column.iloc[-1]
            simetria = Extrapolate_Module.symmetry(df_airfoil)
            if simetria == True:
                if alpha_min_tab < alpha < alpha_max_tab: 
                    Cl, Cd = Interpolate_Extrapolate_Re(alpha, 1000000)
                else:
                    Cl, Cd = Extrapolate_Module.extrapolate_symmetrical(df,df_airfoil,alpha,Re)
            else:
                if alpha_min_tab < alpha < alpha_max_tab: 
                    Cl, Cd = Interpolate_Extrapolate_Re(alpha, 1000000)
                else:
                    Cl, Cd = Extrapolate_Module.extrapolate_asymmetrical(df,df_airfoil,alpha,Re)
    return Cl, Cd

#-----------------------------------------------------------------#
#Cl y Cd corregidos según la influencia del número de Mach
def Cl_Cd_corregido(alpha, Cl, Cd, Mach):

    transonico = False
    supersonico = False

    df_airfoil = pd.read_csv(Datos.archivo_csv)
    espesor = Camber_Module.thickness_max(df_airfoil)
    curvatura_media = Camber_Module.camber_med(df_airfoil)
    alpha_rad = alpha*Datos.pi/180

    Pi = np.pi
    Cl_zero = ((2 * Pi) / ((1 - (0) ** 2) ** 0.5)) * (1 - 0.77 * espesor) * (alpha_rad + 2 * curvatura_media)

    factor_corrector = Cl/Cl_zero
    factor_corrector_sub, factor_corrector_trans, factor_corrector_sup = Factor_Corrector_Module.Factor_corrector_Mach(Mach)

    if Mach <= 0.8:
        transonico = False
        supersonico = False
        Cl_corregido = (((2 * Pi) / ((1 - (Mach) ** 2) ** 0.5)) * (1 - 0.77 * espesor) * (alpha_rad + 2 * curvatura_media))*factor_corrector
    elif Mach < 1.2:
        transonico = True
        supersonico = False
        Cl_corregido_1 = (((2 * Pi) / ((1 - (0.8) ** 2) ** 0.5)) * (1 - 0.77 * espesor) * (alpha_rad + 2 * curvatura_media))*factor_corrector
        Cl_corregido_2 = ((4 * alpha_rad) / ((((1.2) ** 2) - 1) ** 0.5)) * factor_corrector
        Cl_corregido = Cl_corregido_1 + ((Mach - 0.8) / (1.2 - 0.8)) * (Cl_corregido_2 - Cl_corregido_1)    
    else:
        transonico = False
        supersonico = True
        Cl_corregido = ((4 * alpha_rad) / ((((Mach) ** 2) - 1) ** 0.5)) * factor_corrector 
        

    if Mach < 0.8:
        Cd_corregido = Cd * factor_corrector_sub
    elif Mach < 1.25:
        Cd_corregido = Cd * factor_corrector_trans
    else:
        Cd_corregido = Cd * factor_corrector_sup


    return Cl_corregido, Cd_corregido, transonico, supersonico


#-----------------------------------------------------------------#
#PRUEBAS

""" Cl, Cd = Interpolate_Extrapolate(11,54976.867535048)
Cl_co, Cd_co = Cl_Cd_corregido(11,Cl,Cd,1.2)

print('Cl,Cd:',Cl, Cd)
print('Cl_corregido,Cd_corregido:',Cl_co, Cd_co) """

#PLOT

""" valores_Cl = []
valores_Cd = []
valores_alpha = []
Re = 398465

for alpha in range(-180, 180):
    Cl, Cd = Interpolate_Extrapolate(alpha,Re)
    print('alpha,Cl:', alpha, Cl)
    # Agrega los valores a las listas correspondientes
    valores_Cl.append(Cl)
    valores_Cd.append(Cd)
    valores_alpha.append(alpha)

plt.plot(valores_alpha, valores_Cl, color='red')

# Agrega etiquetas y título al gráfico
plt.xlabel('α(°)')
plt.ylabel('Cl')
plt.title('Cl vs α')

# Agrega una leyenda
plt.legend()

# Muestra el gráfico
plt.show() """