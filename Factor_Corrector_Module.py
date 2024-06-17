#-----------------------------------------------------------------#
#Módulo para el cálculo del factor corrector usado en Cl_Cd_corregido (Interpolate_Extrapolate_Module)
#-----------------------------------------------------------------#
#IMPORTS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------#
#
def Factor_corrector_Mach(Mach):

    factores_correctores = {
    0: 1,
    0.8: 1.7885,
    1.05: 2.515,
    1.25: 1.6468,
    2: 1.387}

    #Subsónico

    cte_sub = (factores_correctores[0.8]-1)/(0.8**2)
    F_prima_Cd_sub = 2*cte_sub*0.8

    factor_corrector_sub = (cte_sub*(Mach**2))+1

    #Transónico
    M_08 = 0.8
    M_105 = 1.05
    M_125 = 1.25

    matriz = np.array([
    [M_08**4, M_08**3, M_08**2, M_08, 1],
    [M_105**4, M_105**3, M_105**2, M_105, 1],
    [M_125**4, M_125**3, M_125**2, M_125, 1],
    [4*(M_08)**3, 3*(M_08)**2, 2*M_08, 1, 0],
    [4*(M_105)**3, 3*(M_105)**2, 2*M_105, 1, 0]
    ])

    matriz_inversa = np.linalg.inv(matriz)

    matriz_2 = np.array([
    [factores_correctores[0.8]],
    [factores_correctores[1.05]],
    [factores_correctores[1.25]],
    [F_prima_Cd_sub],
    [0]
    ])

    abcde = np.matmul(matriz_inversa, matriz_2)
    A = abcde[0].item()
    B = abcde[1].item()
    C = abcde[2].item()
    D = abcde[3].item()
    E = abcde[4].item()

    F_prima_Cd_trans = 4*A*(1.25**3)+3*B*(1.25**2)+2*C*1.25+D

    factor_corrector_trans = A*(Mach**4)+B*(Mach**3)+C*(Mach**2)+D*Mach+E

    #Supersónico

    G = factores_correctores[2]
    J = -F_prima_Cd_trans/(factores_correctores[1.25]-factores_correctores[2])
    H = (factores_correctores[1.25]-factores_correctores[2])/(np.exp(-J*1.25))

    factor_corrector_sup = G+H*np.exp(-J*Mach)

    return factor_corrector_sub, factor_corrector_trans, factor_corrector_sup

#-----------------------------------------------------------------#
