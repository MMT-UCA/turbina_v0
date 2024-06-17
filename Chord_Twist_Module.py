#-----------------------------------------------------------------#
#MÓDULO CUERDA-TORSIÓN VARIABLES
#Cálculos de cuerda y torsión variables (o fijas)
#-----------------------------------------------------------------#
#IMPORTS
import math
import pandas as pd
import matplotlib.pyplot as plt
from Datos import Datos
import numpy as np
#-----------------------------------------------------------------#

#TORSIÓN
#Esta función lee en Datos si la torsión es variable o fija. Si es variable coge los datos de Beta para cada radio
#y crea a partir de ellos una lista de Beta_crucero desde r_o hasta D/2 en pasos de dr, y el valor de Beta_n_crucero
#a 3/4 del radio

def Torsion():

    if Datos.torsion_variable == True:

        df = pd.read_csv(Datos.torsion_csv)
        r_datos = df['radio']
        Beta_datos = df['Beta']

        Beta_crucero = []
        r = Datos.r_o
        r_puntomedio = r + (Datos.dr / 2)
        r_34 = (((Datos.D/2))-Datos.r_o)*(3/4)
        while r <= (Datos.D)/2:
            if r_puntomedio in r_datos.values:
                # Obtener el índice del valor de r en la columna
                idx = r_datos[r_datos == r_puntomedio].index[0]
                # Obtener el valor correspondiente de Beta
                valor = df.loc[idx, 'Beta']
                if r_puntomedio == r_34:
                    Beta_n_crucero = valor
            else:
                # Encontrar el valor inmediatamente superior en la lista
                r_upper = r_datos[r_datos >= r_puntomedio].min()
                # Encontrar el valor inmediatamente inferior en la lista
                r_lower = r_datos[r_datos <= r_puntomedio].max()
                # Obtener los valores de Beta correspondientes a los r encontrados
                Beta_lower = Beta_datos[r_datos == r_lower].iloc[0] if not pd.isnull(r_lower) else None
                Beta_upper = Beta_datos[r_datos == r_upper].iloc[0] if not pd.isnull(r_upper) else None
                valor = Beta_lower + ((Beta_upper-Beta_lower)/(r_upper-r_lower))*(r_puntomedio-r_lower)
                if r_upper > r_34 and r_lower < r_34:
                    Beta_n_crucero = Beta_lower + ((Beta_upper-Beta_lower)/(r_upper-r_lower))*(r_34-r_lower)
            Beta_crucero.append(valor)
            r += Datos.dr
            r_puntomedio += Datos.dr
        

    else:

        alfa_rad = Datos.alfa_diseno * (math.pi / 180) #radianes
        n = Datos.RPM / 60 #rps
        C_crucero_ms = Datos.C_crucero *(1000/3600)

        j = C_crucero_ms / (n * Datos.D)

        Beta_crucero = [] # Definir Beta_crucero como una lista vacía

        r = Datos.r_o
        while r <= (Datos.D)/2:
            valor = (math.atan(Datos.D * j / (2 * math.pi * r)) + alfa_rad) * (180 / math.pi)
            Beta_crucero.append(valor)
            r += Datos.dr

        Beta_n_crucero = (math.atan(Datos.D * j / (2 * math.pi * 3 * Datos.D / 8)) + alfa_rad) * 180 / math.pi
    return Beta_crucero, Beta_n_crucero


#-----------------------------------------------------------------#

#CUERDA
#Esta función lee en Datos si la cuerda es variable o fija. Si es variable coge los datos de cuerda para cada radio
#y crea a partir de ellos una lista de valores de cuerda desde r_o hasta D/2 en pasos de dr, y el valor de la cuerda media

def cuerda():

    df = pd.read_csv(Datos.cuerda_csv)
    r_datos = df['radio']
    cuerda_datos = df['cuerda']

    valor_cuerda = []
    r = Datos.r_o
    r_puntomedio = r + (Datos.dr / 2)

    if Datos.cuerda_variable == True:

        while r <= (Datos.D)/2:
            if r_puntomedio in r_datos.values:
                # Obtener el índice del valor de r en la columna
                idx = r_datos[r_datos == r_puntomedio].index[0]
                # Obtener el valor correspondiente de cuerda
                valor = df.loc[idx, 'cuerda']
            else:
                # Encontrar el valor inmediatamente superior en la lista
                r_upper = r_datos[r_datos >= r_puntomedio].min()
                # Encontrar el valor inmediatamente inferior en la lista
                r_lower = r_datos[r_datos <= r_puntomedio].max()
                # Obtener los valores de cuerda correspondientes a los r encontrados
                cuerda_lower = cuerda_datos[r_datos == r_lower].iloc[0] if not pd.isnull(r_lower) else None
                cuerda_upper = cuerda_datos[r_datos == r_upper].iloc[0] if not pd.isnull(r_upper) else None
                valor = cuerda_lower + ((cuerda_upper-cuerda_lower)/(r_upper-r_lower))*(r_puntomedio-r_lower)
            valor_cuerda.append(valor)
            r += Datos.dr
            r_puntomedio += Datos.dr

        valor_cuerda_media = np.mean(valor_cuerda)

    else:
        
        while r <= ((Datos.D)/2 + (Datos.dr / 2)):
            valor = Datos.cuerda_fija
            valor_cuerda.append(valor)
            r += Datos.dr
        valor_cuerda_media = valor

    return valor_cuerda, valor_cuerda_media

#-----------------------------------------------------------------#