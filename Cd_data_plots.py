#-----------------------------------------------------------------#
#Grafica Cd vs α
#-----------------------------------------------------------------#
#IMPORTS

import pandas as pd
import matplotlib.pyplot as plt
import Datos

#-----------------------------------------------------------------#

# Lee los datos desde el archivo CSV
df = pd.read_csv(Datos.url_Re50000, skiprows=10)
df_2 = pd.read_csv(Datos.url_Re100000, skiprows=10)
df_3 = pd.read_csv(Datos.url_Re200000, skiprows=10)
df_4 = pd.read_csv(Datos.url_Re500000, skiprows=10)
df_5 = pd.read_csv(Datos.url_Re1000000, skiprows=10)

#-----------------------------------------------------------------#
#Cd vs α

# Extrae las columnas X e Y
columna_x = df['Alpha']
columna_y = df['Cd']
columna_x_2 = df_2['Alpha']
columna_y_2 = df_2['Cd']
columna_x_3 = df_3['Alpha']
columna_y_3 = df_3['Cd']
columna_x_4 = df_4['Alpha']
columna_y_4 = df_4['Cd']
columna_x_5 = df_5['Alpha']
columna_y_5 = df_5['Cd']

# Crea un gráfico de puntos
plt.scatter(columna_x, columna_y, color='cornflowerblue',label='Re50000')
plt.scatter(columna_x_2, columna_y_2, color='yellow',label='Re100000')
plt.scatter(columna_x_3, columna_y_3, color='green',label='Re200000')
plt.scatter(columna_x_4, columna_y_4, color='navy',label='Re500000')
plt.scatter(columna_x_5, columna_y_5, color='orange',label='Re1000000')

# Establecer límites en los ejes x e y
#plt.xlim(-10, 15)  # Límites en el eje x desde 0 hasta 6
#plt.ylim(0, 0.12)  # Límites en el eje y desde 0 hasta 10

# Agrega etiquetas y título al gráfico
plt.xlabel('Alpha(°)')
plt.ylabel('Cd')
plt.title('Cd vs α')

plt.legend()

# Muestra el gráfico
plt.show()