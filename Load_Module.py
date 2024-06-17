#-----------------------------------------------------------------#
#MÓDULO LOAD
#Carga de datos
#-----------------------------------------------------------------#
#IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
from Datos import Datos
import numpy as np
import globals
#-----------------------------------------------------------------#


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


