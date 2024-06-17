#-----------------------------------------------------------------#
#MÓDULO PRINCIPAL
#-----------------------------------------------------------------#
#IMPORTS
from Datos import Datos
import Helice_Module
import Aircraft_Module

#-----------------------------------------------------------------#
#Cálculo .csv T-C, W-C, eta-C, Ct-J, Cp-J de Módulo Hélice

valores_beta = [10, 20, 30, 40, 50, 60, 70, 80]

Helice_Module.csv_complete(valores_beta)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#Plot de T-C, W-C, eta-C

valores_plot_beta = [10, 20, 30, 40, 50, 60]

Helice_Module.plot_complete(valores_plot_beta)

#-----------------------------------------------------------------#
#Cálculo .csv t, x, C, a, Fd, T ,W de Módulo Avión

Aircraft_Module.csv_principal()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#Plot de T-C, W-C, eta-C

Aircraft_Module.plot_complete_aircraft()

#-----------------------------------------------------------------#