#-----------------------------------------------------------------#
#MÓDULO DE EXTRAPOLACIÓN SEGÚN LA POLAR DE LORENZO BATTISTI
#-----------------------------------------------------------------#
#IMPORTS

import pandas as pd
import matplotlib.pyplot as plt
from Datos import Datos
import math
import Camber_Module
import Chord_Twist_Module

#Extrapolación de la polar de Lorenzo Battisti et al https://doi.org/10.1016/j.renene.2020.03.15
#-----------------------------------------------------------------#

#Se calcula si el perfil es simétrico a partir de las coordenadas
def symmetry(df):

    # Calcular la media de las coordenadas y
    media_y = df['y'].mean()
    
    # Verificar si el perfil es simétrico
    es_simetrico = all(abs(df['y'] - media_y) < 1e-6)  # Tolerancia para evitar errores de redondeo
    
    return es_simetrico

#-----------------------------------------------------------------#

#Se calcula el ángulo de sustentación nula
def alpha_zero(df):

    alpha_column = df['Alpha'].tolist()
    Cl_column = df['Cl'].tolist()

    indice_ultimo_negativo = Cl_column.index(next(valor for valor in Cl_column if valor < 0))
    indice_primer_positivo = indice_ultimo_negativo + 1

    while indice_primer_positivo < len(Cl_column) and Cl_column[indice_primer_positivo] <= 0:
        indice_primer_positivo += 1
    
    indice_ultimo_negativo = indice_primer_positivo - 1
    
    Cl_negativo = Cl_column[indice_ultimo_negativo]
    Cl_positivo = Cl_column[indice_primer_positivo]
    alpha_negativo = alpha_column[indice_ultimo_negativo]
    alpha_positivo = alpha_column[indice_primer_positivo]

    alphazero = alpha_positivo - Cl_positivo*((alpha_positivo-alpha_negativo)/(Cl_positivo-Cl_negativo))

    return alphazero 

#-----------------------------------------------------------------#

#Función principal de extrapolación, según la simetría del perfil llama a la función correspondiente
def extrapolate(df,df_airfoil,alpha,Re):
    if symmetry(df_airfoil):
        Cl, Cd = extrapolate_symmetrical(df,df_airfoil,alpha,Re)
    else:
        Cl, Cd = extrapolate_asymmetrical(df,df_airfoil,alpha,Re)
    return Cl, Cd


#-----------------------------------------------------------------#

def extrapolate_asymmetrical(df,df_airfoil,alpha,Re):

    alpha_column = df['Alpha']
    alpha_min_tab = alpha_column.iloc[1]
    alpha_max_tab = alpha_column.iloc[-1]
    Cl_column = df['Cl']
    Cl_min_tab = Cl_column.iloc[1]
    Cl_max_tab = Cl_column.iloc[-1]
    Cd_column = df['Cd']
    Cd_min_tab = Cd_column.iloc[1]
    Cd_max_tab = Cd_column.iloc[-1]

    t_c = Camber_Module.thickness_max(df_airfoil)
    h_c = Camber_Module.camber_max(df_airfoil)

    alphazero = alpha_zero(df)

    valor_cuerda, valor_cuerda_media = Chord_Twist_Module.cuerda()
    AR = Datos.D / valor_cuerda_media

    if alpha < alpha_min_tab : #alpha menor que el mínimo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        CD_270 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c - 1.39 * h_c
        beta_prim = alpha - alphazero * math.cos(alpha * math.pi / 180)
        CD_func = (CD_90 + CD_270)/2 + ((CD_90 - CD_270) / 2) * math.sin(beta_prim * math.pi / 180)
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_func) * ((math.sin(alpha * math.pi / 180)) + 0.0023 * (math.sin(2 * alpha * math.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * math.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_func) * 0.3 * t_c * (abs(math.sin(alpha * math.pi / 180) + 0.1 * math.sin(2 * alpha * math.pi / 180))) * (1 - 2 * math.cos(alpha * math.pi / 180)) - CD_f * math.cos(alpha * math.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl = CN * math.cos(alpha * math.pi / 180) + CT * math.sin(alpha * math.pi / 180)
        Cd = (CN * math.sin(alpha * math.pi / 180) - CT * math.cos(alpha * math.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (AR/ (math.sin(alpha * math.pi / 180))))))
        if alpha >= -45 and alpha <= alpha_min_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_menos = ((Cl_min_tab / math.cos(alpha_min_tab * math.pi / 180)) - (Cd_min_tab / math.sin(alpha_min_tab * math.pi / 180))) / ((math.sin(alpha_min_tab * math.pi / 180) / math.cos(alpha_min_tab * math.pi / 180)) + (math.cos(alpha_min_tab * math.pi / 180) / math.sin(alpha_min_tab * math.pi / 180)))
            CN_ds_menos = (Cl_min_tab - (CT_ds_menos * math.sin(alpha_min_tab * math.pi / 180))) / (math.cos(alpha_min_tab * math.pi / 180))
            beta_prim = -45 - alphazero * math.cos(-45 * math.pi / 180)
            CD_func = (CD_90 + CD_270)/2 + ((CD_90 - CD_270) / 2) * math.sin(beta_prim * math.pi / 180)
            f_menos = ((alpha + 45) / (alpha_min_tab + 45)) ** 2
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_func) * ((math.sin(-45 * math.pi / 180)) + 0.0023 * (math.sin(2 * -45 * math.pi / 180)) / (0.38 + (0.62 * abs((math.sin(-45 * math.pi / 180)))) + (3.7 * t_c * ((math.cos(-45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_func) * 0.3 * t_c * (abs(math.sin(-45 * math.pi / 180) + 0.1 * math.sin(2 * -45 * math.pi / 180))) * (1 - 2 * math.cos(-45 * math.pi / 180)) - CD_f * math.cos(-45 * math.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_menos = CN_ds_menos * f_menos + CN_sep * (1 - f_menos)
            CT_menos = CT_ds_menos * f_menos + CT_sep * (1 - f_menos)
            #Coeficientes de sustentación y resistencia
            Cl = CN_menos * math.cos(alpha * math.pi / 180) + CT_menos * math.sin(alpha * math.pi / 180)
            Cd = (CN_menos * math.sin(alpha * math.pi / 180) - CT_menos * math.cos(alpha * math.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (AR/ (math.sin(alpha * math.pi / 180))))))
            
    else:  #alpha mayor que el máximo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        CD_270 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c - 1.39 * h_c
        beta_prim = alpha - alphazero * math.cos(alpha * math.pi / 180)
        CD_func = (CD_90 + CD_270)/2 + ((CD_90 - CD_270) / 2) * math.sin(beta_prim * math.pi / 180)
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_func) * ((math.sin(alpha * math.pi / 180)) + 0.0023 * (math.sin(2 * alpha * math.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * math.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_func) * 0.3 * t_c * (abs(math.sin(alpha * math.pi / 180) + 0.1 * math.sin(2 * alpha * math.pi / 180))) * (1 - 2 * math.cos(alpha * math.pi / 180)) - CD_f * math.cos(alpha * math.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl = CN * math.cos(alpha * math.pi / 180) + CT * math.sin(alpha * math.pi / 180)
        Cd = (CN * math.sin(alpha * math.pi / 180) - CT * math.cos(alpha * math.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (AR/ (math.sin(alpha * math.pi / 180))))))
        if alpha <= 45 and alpha >= alpha_max_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_mas = ((Cl_max_tab / math.cos(alpha_max_tab * math.pi / 180)) - (Cd_max_tab / math.sin(alpha_max_tab * math.pi / 180))) / ((math.sin(alpha_max_tab * math.pi / 180) / math.cos(alpha_max_tab * math.pi / 180)) + (math.cos(alpha_max_tab * math.pi / 180) / math.sin(alpha_max_tab * math.pi / 180)))
            CN_ds_mas = (Cl_max_tab - (CT_ds_mas * math.sin(alpha_max_tab * math.pi / 180))) / (math.cos(alpha_max_tab * math.pi / 180))
            f_mas = ((alpha - 45) / (alpha_max_tab - 45)) ** 2
            beta_prim = 45 - alphazero * math.cos(45 * math.pi / 180)
            CD_func = (CD_90 + CD_270)/2 + ((CD_90 - CD_270) / 2) * math.sin(beta_prim * math.pi / 180)
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_func) * ((math.sin(45 * math.pi / 180)) + 0.0023 * (math.sin(2 * 45 * math.pi / 180)) / (0.38 + (0.62 * abs((math.sin(45 * math.pi / 180)))) + (3.7 * t_c * ((math.cos(45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_func) * 0.3 * t_c * (abs(math.sin(45 * math.pi / 180) + 0.1 * math.sin(2 * 45 * math.pi / 180))) * (1 - 2 * math.cos(45 * math.pi / 180)) - CD_f * math.cos(45 * math.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_mas = CN_ds_mas * f_mas + CN_sep * (1 - f_mas)
            CT_mas = CT_ds_mas * f_mas + CT_sep * (1 - f_mas)
            #Coeficientes de sustentación y resistencia
            Cl = CN_mas * math.cos(alpha * math.pi / 180) + CT_mas * math.sin(alpha * math.pi / 180)
            Cd = (CN_mas * math.sin(alpha * math.pi / 180) - CT_mas * math.cos(alpha * math.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (AR/ (math.sin(alpha * math.pi / 180))))))

    return Cl, Cd

#-----------------------------------------------------------------#

def extrapolate_symmetrical(df,df_airfoil,alpha,Re):

    alpha_column = df['Alpha']
    alpha_min_tab = alpha_column.iloc[1]
    alpha_max_tab = alpha_column.iloc[-1]
    Cl_column = df['Cl']
    Cl_min_tab = Cl_column.iloc[1]
    Cl_max_tab = Cl_column.iloc[-1]
    Cd_column = df['Cd']
    Cd_min_tab = Cd_column.iloc[1]
    Cd_max_tab = Cd_column.iloc[-1]

    t_c = Camber_Module.thickness_max(df_airfoil)
    h_c = Camber_Module.camber_max(df_airfoil)

    valor_cuerda, valor_cuerda_media = Chord_Twist_Module.cuerda()
    AR = Datos.D / valor_cuerda_media

    if alpha < alpha_min_tab : #alpha menor que el mínimo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_90) * ((math.sin(alpha * math.pi / 180)) + 0.0023 * (math.sin(2 * alpha * math.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * math.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_90) * 0.3 * t_c * (abs(math.sin(alpha * math.pi / 180) + 0.1 * math.sin(2 * alpha * math.pi / 180))) * (1 - 2 * math.cos(alpha * math.pi / 180)) - CD_f * math.cos(alpha * math.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl = CN * math.cos(alpha * math.pi / 180) + CT * math.sin(alpha * math.pi / 180)
        Cd = (CN * math.sin(alpha * math.pi / 180) - CT * math.cos(alpha * math.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (AR/ (math.sin(alpha * math.pi / 180))))))
        if alpha >= -45 and alpha <= alpha_min_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_menos = ((Cl_min_tab / math.cos(alpha_min_tab * math.pi / 180)) - (Cd_min_tab / math.sin(alpha_min_tab * math.pi / 180))) / ((math.sin(alpha_min_tab * math.pi / 180) / math.cos(alpha_min_tab * math.pi / 180)) + (math.cos(alpha_min_tab * math.pi / 180) / math.sin(alpha_min_tab * math.pi / 180)))
            CN_ds_menos = (Cl_min_tab - (CT_ds_menos * math.sin(alpha_min_tab * math.pi / 180))) / (math.cos(alpha_min_tab * math.pi / 180))
            f_menos = ((alpha + 45) / (alpha_min_tab + 45)) ** 2
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_90) * ((math.sin(-45 * math.pi / 180)) + 0.0023 * (math.sin(2 * -45 * math.pi / 180)) / (0.38 + (0.62 * abs((math.sin(-45 * math.pi / 180)))) + (3.7 * t_c * ((math.cos(-45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_90) * 0.3 * t_c * (abs(math.sin(-45 * math.pi / 180) + 0.1 * math.sin(2 * -45 * math.pi / 180))) * (1 - 2 * math.cos(-45 * math.pi / 180)) - CD_f * math.cos(-45 * math.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_menos = CN_ds_menos * f_menos + CN_sep * (1 - f_menos)
            CT_menos = CT_ds_menos * f_menos + CT_sep * (1 - f_menos)
            #Coeficientes de sustentación y resistencia
            Cl = CN_menos * math.cos(alpha * math.pi / 180) + CT_menos * math.sin(alpha * math.pi / 180)
            Cd = (CN_menos * math.sin(alpha * math.pi / 180) - CT_menos * math.cos(alpha * math.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (AR/ (math.sin(alpha * math.pi / 180))))))
            
    else:  #alpha mayor que el máximo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_90) * ((math.sin(alpha * math.pi / 180)) + 0.0023 * (math.sin(2 * alpha * math.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * math.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_90) * 0.3 * t_c * (abs(math.sin(alpha * math.pi / 180) + 0.1 * math.sin(2 * alpha * math.pi / 180))) * (1 - 2 * math.cos(alpha * math.pi / 180)) - CD_f * math.cos(alpha * math.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl = CN * math.cos(alpha * math.pi / 180) + CT * math.sin(alpha * math.pi / 180)
        Cd = (CN * math.sin(alpha * math.pi / 180) - CT * math.cos(alpha * math.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (AR/ (math.sin(alpha * math.pi / 180))))))
        if alpha <= 45 and alpha >= alpha_max_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_mas = ((Cl_max_tab / math.cos(alpha_max_tab * math.pi / 180)) - (Cd_max_tab / math.sin(alpha_max_tab * math.pi / 180))) / ((math.sin(alpha_max_tab * math.pi / 180) / math.cos(alpha_max_tab * math.pi / 180)) + (math.cos(alpha_max_tab * math.pi / 180) / math.sin(alpha_max_tab * math.pi / 180)))
            CN_ds_mas = (Cl_max_tab - (CT_ds_mas * math.sin(alpha_max_tab * math.pi / 180))) / (math.cos(alpha_max_tab * math.pi / 180))
            f_mas = ((alpha - 45) / (alpha_max_tab - 45)) ** 2
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_90) * ((math.sin(45 * math.pi / 180)) + 0.0023 * (math.sin(2 * 45 * math.pi / 180)) / (0.38 + (0.62 * abs((math.sin(45 * math.pi / 180)))) + (3.7 * t_c * ((math.cos(45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_90) * 0.3 * t_c * (abs(math.sin(45 * math.pi / 180) + 0.1 * math.sin(2 * 45 * math.pi / 180))) * (1 - 2 * math.cos(45 * math.pi / 180)) - CD_f * math.cos(45 * math.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_mas = CN_ds_mas * f_mas + CN_sep * (1 - f_mas)
            CT_mas = CT_ds_mas * f_mas + CT_sep * (1 - f_mas)
            #Coeficientes de sustentación y resistencia
            Cl = CN_mas * math.cos(alpha * math.pi / 180) + CT_mas * math.sin(alpha * math.pi / 180)
            Cd = (CN_mas * math.sin(alpha * math.pi / 180) - CT_mas * math.cos(alpha * math.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (AR/ (math.sin(alpha * math.pi / 180))))))

    return Cl, Cd

#-----------------------------------------------------------------#

