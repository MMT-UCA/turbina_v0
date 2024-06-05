#-----------------------------------------------------------------#
#MÓDULO PERFIL VARIABLE
#Cálculos de perfil variable
#-----------------------------------------------------------------#
#IMPORTS
import math
import pandas as pd
import matplotlib.pyplot as plt
import Datos
import numpy as np
import globals
#-----------------------------------------------------------------#


""" def load_Re(df_csv_variable):

    df_Re_list = []
    nombre_df_Re_list = []
    for index, row in df_csv_variable.iterrows():
        nombre_perfil = row['perfil']
        for Re in [50000, 100000, 200000, 500000, 1000000]:
            nombre_archivo_Re = 'Datos.url__' + nombre_perfil + '_Re' + str(Re)
            archivo_Re = eval(nombre_archivo_Re)
            df_Re = pd.read_csv(archivo_Re,skiprows=10)
            df_Re_list.append(df_Re)
            nombre_df = 'df_' + nombre_perfil + '_Re' + str(Re)
            nombre_df_Re_list.append(nombre_df)
            
    return df_Re_list, nombre_df_Re_list """

def load_Re(df_csv_variable):

    load_Re_map:map = {}
    for index, row in df_csv_variable.iterrows():
        nombre_perfil = row['perfil']
        for Re in [50000, 100000, 200000, 500000, 1000000]:
            nombre_archivo_Re = 'Datos.url__' + nombre_perfil + '_Re' + str(Re)
            archivo_Re = eval(nombre_archivo_Re)
            df_Re = pd.read_csv(archivo_Re,skiprows=10)
            nombre_df = 'df_' + nombre_perfil + '_Re' + str(Re)
            load_Re_map[nombre_df] = df_Re
            globals.global_vars[nombre_df] = df_Re

    return load_Re_map


""" df_csv_variable = pd.read_csv(Datos.archivo_csv_variable)
load_Re_map = load_Re(df_csv_variable)
#print(load_Re_map)
x = 'df_NACA0012_Re50000'
print(globals()[x]) """


""" for row in df_Re_list.iterrows():
    nombre_perfil = row['perfil']
    for Re in [50000, 100000, 200000, 500000, 1000000]:
        nombre_df = 'df_' + nombre_perfil + '_Re' + str(Re)
        archivo_Re = eval(nombre_archivo_Re)
        df_Re = pd.read_csv(archivo_Re,skiprows=10)
        df_Re_list.append(df_Re)
        archivo_Re = eval(nombre_archivo_Re) """
