#-----------------------------------------------------------------#
#Archivo de datos de entrada
#-----------------------------------------------------------------#
#DATOS AVIÓN

#Avión: Piagio 180 avanti
m = 5216 #kg
n_motor = 2
C_d = 0.02
A_a = 16 #m^2
C_crucero = 593 #km/h
dt = 1 #s
dt_acel = 1 #s
t_fin = 60 #s
t_fin_acel = 10 #s
Z = 0 #m
C = 0
x = 0

#-----------------------------------------------------------------#

#DATOS GLOBALES

pi = 3.141592654

#-----------------------------------------------------------------#

#DATOS HÉLICE

Beta = 60 #°
D = 2.2 #m
r_o = 0.15 #m
RPM = 2000 
RPS = RPM/60 #equivalente a n de Excel
#AR = D/cuerda
Palas = 5 
dr = 0.1 #m

error_helice = 0.1
omega = 2*pi*RPS
Ah = pi*(D**2)/4

#CUERDA

#Si la cuerda es variable indicar True y proporcionar .csv con los datos de cuerda (radio, cuerda), 
#el primer valor de radio deberá ser r_o indicado anteriormente, y el último D/2
#Si la cuerda no varía indicar False, e indicar el valor de cuerda_fija

cuerda_variable = True

cuerda_csv = "datos_cuerda_2.csv"

cuerda_fija = 0.1 #m

#-----------------------------------------------------------------#

#DATOS VELOCIDADES INDUCIDAS

m_vind = 1
a_vind = 1
n_vind = 0.2

#-----------------------------------------------------------------#

#DATOS TORSIÓN

#Si la torsión es variable indicar True y proporcionar .csv con los datos de torsión (radio, Beta), 
#el primer valor de radio deberá ser r_o indicado anteriormente, y el último D/2
#Si la torsión no varía indicar False

torsion_variable = True

torsion_csv = "datos_torsion_2.csv"

alfa_diseno = 5 #°

#-----------------------------------------------------------------#

#URLs

#Re50000

#url_Re50000="http://airfoiltools.com/polar/csv?polar=xf-naca2411-il-50000"
url_Re50000="xf-naca2411-il-50000.csv"

#Re100000

#url_Re100000="http://airfoiltools.com/polar/csv?polar=xf-naca2411-il-100000"
url_Re100000="xf-naca2411-il-100000.csv"
#Re200000

#url_Re200000="http://airfoiltools.com/polar/csv?polar=xf-naca2411-il-200000"
url_Re200000="xf-naca2411-il-200000.csv"

#Re500000

#url_Re500000="http://airfoiltools.com/polar/csv?polar=xf-naca2411-il-500000"
url_Re500000="xf-naca2411-il-500000.csv"

#Re1000000

#url_Re1000000="http://airfoiltools.com/polar/csv?polar=xf-naca2411-il-1000000"
url_Re1000000="xf-naca2411-il-1000000.csv"

#Coordenadas

archivo_csv = "Coordenadas.csv"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

#Resultados

T_C_csv = "T_C_cuerdatorsion_var.csv"

W_C_csv = "W_C_cuerdatorsion_var.csv"

eta_C_csv = "eta_C_cuerdatorsion_var.csv"

Ct_J_csv = "Ct_J_cuerdatorsion_var.csv"

Cp_J_csv = "Cp_J_cuerdatorsion_var.csv"

resultados_principal_csv = "resultados_principal.csv"

