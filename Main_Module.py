#-----------------------------------------------------------------#
#INACABADO
#IMPORTS

import math
import Datos

#-----------------------------------------------------------------#

#DEFINICIÓN VARIABLES GLOBALES

#-----------------------------------------------------------------#

#FUNCIONES

def Temp(Z) :
    if Z < 11000 :
        return 288.19 - 0.00649*Z
    elif Z < 25000 :
        return 216.69
    else :
        return 141.94 + 0.00299*Z
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

def Pres(Z) :
    if Z < 11000 :
        return 101.29 * (Temp(Z) / 288.08) ^ 5.256
    elif Z < 25000 :
        return 22.65 * math.exp(1.73 - 0.000157 * Z)
    else :
        return 2.488 * (Temp(Z) / 216.6) ^ -11.388

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

def rho(Z) :
    return Pres(Z)/(0.287*Temp(Z))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #








#-----------------------------------------------------------------#
#PRUEBAS

Z = 22000
temperatura_resultante = Temp(Z)
pres_resultante = Pres(Z)
den_resultante = rho(Z)
Beta = Datos.Beta

print(f"Altitud: {Z} metros")
print(f"Temperatura: {temperatura_resultante} K") 
print(f"Presión: {pres_resultante} kPa") 
print(f"Densidad: {den_resultante} kg/m^3") 
print(f"Beta: {Beta}")


"""
Z = 22000
temperatura_resultante = Temp(Z)
pres_resultante = Pres(Z)

print(f"Altitud: {Z} metros")
print(f"Temperatura: {temperatura_resultante} K") 
print(f"Presión: {pres_resultante} kPa") 

"""