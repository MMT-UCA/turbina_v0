
#DATOS AVIÓN

#Avión: Piagio 180 avanti
m = 5216 #kg
n_motor = 2
C_d = 0.02
A_a = 16 #m^2
C_crucero = 593 #km/h
dt = 1 #s
t_fin = 600 #s
Z = 22000 #m
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
cuerda = 0.1 #m
RPM = 2000 
RPS = RPM/60 #equivalente a n de Excel
AR = D/cuerda
Palas = 5 
dr = 0.01 #m

error_helice = 0.1
omega = 2*pi*RPS
Ah = pi*(D**2)/4

#-----------------------------------------------------------------#

#DATOS VELOCIDADES INDUCIDAS

m_vind = 1
a_vind = 1
n_vind = 0.2

#-----------------------------------------------------------------#

#DATOS TORSIÓN

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

url_Re200000="http://airfoiltools.com/polar/csv?polar=xf-naca2411-il-200000"

#Re500000

url_Re500000="http://airfoiltools.com/polar/csv?polar=xf-naca2411-il-500000"

#Re1000000

url_Re1000000="http://airfoiltools.com/polar/csv?polar=xf-naca2411-il-1000000"

#Coordenadas

archivo_csv = "/Users/albacrespogonzalez/Desktop/TFG/Python/Coordenadas.csv"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

