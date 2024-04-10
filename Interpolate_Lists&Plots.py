#IMPORTS

import pandas as pd
import matplotlib.pyplot as plt
import Datos

#-----------------------------------------------------------------#

# Lee los datos desde el archivo CSV
df = pd.read_csv(Datos.url_Re50000, skiprows=10)

# Extraer las columnas x y y_list
x_list = df['Alpha']
y_list = df['Cl']

# Lee los datos desde el archivo CSV
df_2 = pd.read_csv(Datos.url_Re100000, skiprows=10)

# Extraer las columnas x y y_list
x_list_2 = df_2['Alpha']
y_list_2 = df_2['Cl']

# Lee los datos desde el archivo CSV
df_3 = pd.read_csv(Datos.url_Re200000, skiprows=10)

# Extraer las columnas x y y_list
x_list_3 = df_3['Alpha']
y_list_3 = df_3['Cl']

# Lee los datos desde el archivo CSV
df_4 = pd.read_csv(Datos.url_Re500000, skiprows=10)

# Extraer las columnas x y y_list
x_list_4 = df_4['Alpha']
y_list_4 = df_4['Cl']

# Lee los datos desde el archivo CSV
df_5 = pd.read_csv(Datos.url_Re1000000, skiprows=10)

# Extraer las columnas x y y_list
x_list_5 = df_5['Alpha']
y_list_5 = df_5['Cl']

# Precisión deseada para alpha
precision_alpha = Datos.paso_alfa

# Precisión deseada para Reynolds
precision_Re = Datos.paso_Re

#-----------------------------------------------------------------#

def interpolate(x_1,y_1,x_2,y_2,x_3):

    y_3 = y_1 + ((y_2-y_1)/(x_2-x_1))*(x_3-x_1)

    return y_3

#-----------------------------------------------------------------#


def interpolate_list(x_list,y_list,precision_x):

    # Valores iniciales y finales de x
    x_inicial = x_list[0]
    x_final = x_list.iloc[-1]

    # Crear lista de x_nuevo
    x_nuevo = []
    current_x = x_inicial
    while current_x <= x_final:
        x_nuevo.append(current_x)
        if current_x in x_list.tolist():  # Si el valor de x ya está en la lista de x_list conocidos
            current_x += precision_x  # Incrementar x sin realizar interpolación
        else:
            current_x = round(current_x + precision_x, 6)  # Realizar interpolación y redondear

    # Crear lista de y_nuevo
    y_nuevo = []
    for i, x in enumerate(x_nuevo):
        if x in x_list.tolist():  # Si el valor de x ya está en la lista de x_list conocidos
         y_nuevo.append(y_list[x_list.tolist().index(x)])  # Agregar el valor conocido de y_list
        else:
            # Encontrar el x más cercano en la lista de x_list conocidos
            x_m = max(filter(lambda a: a < x, x_list.tolist()))
            x_a = min(filter(lambda a: a > x, x_list.tolist()))
            index_m = x_list.tolist().index(x_m)
            index_a = x_list.tolist().index(x_a)
            # Realizar la interpolación
            y_list_interpolated = interpolate(x_m, y_list[index_m], x_a, y_list[index_a], x)
            y_nuevo.append(y_list_interpolated)

    return x_nuevo, y_nuevo

#-----------------------------------------------------------------#

def interpolate_Re(Re, Cl, Re_precision):
    Re_nuevo = list(range(Re[0], Re[-1] + Re_precision, Re_precision))
    lista_cl_nuevo = []
    for r in Re_nuevo:
        if r <= Re[0]:
            lista_cl_nuevo.append(Cl[0])
        elif r >= Re[-1]:
            lista_cl_nuevo.append(Cl[-1])
        else:
            index = next(i for i, val in enumerate(Re) if val > r)
            x1, y1 = Re[index - 1], Cl[index - 1]
            x2, y2 = Re[index], Cl[index]
            interpolated_cl = [interpolate(x1, y1[i], x2, y2[i], r) for i in range(len(y1))]
            lista_cl_nuevo.append(interpolated_cl)
    return Re_nuevo, lista_cl_nuevo


#-----------------------------------------------------------------#

#CÁLCULO DE CL

alpha_list, Cl_Re50000 = interpolate_list(x_list,y_list,precision_alpha)
alpha_list_2, Cl_Re100000 = interpolate_list(x_list_2,y_list_2,precision_alpha)
alpha_list_3, Cl_Re200000 = interpolate_list(x_list_3,y_list_3,precision_alpha)
alpha_list_4, Cl_Re500000 = interpolate_list(x_list_4,y_list_4,precision_alpha)
alpha_list_5, Cl_Re1000000 = interpolate_list(x_list_5,y_list_5,precision_alpha)

Re_list = [50000, 100000, 200000, 500000, 1000000]
Cl_list = [Cl_Re50000, Cl_Re100000, Cl_Re200000, Cl_Re500000, Cl_Re1000000]

Re_list_new, Cl_lists = interpolate_Re(Re_list,Cl_list, precision_Re)

#-----------------------------------------------------------------#

#PLOT

#plt.scatter(alpha_list, Cl_lists[0], color='red', label='Re=' + str(Re_list_new[0]))
#plt.scatter(alpha_list, Cl_lists[1], color='green', label='Re=' + str(Re_list_new[1]))
#plt.scatter(alpha_list, Cl_lists[3], color='cornflowerblue', label='Re=' + str(Re_list_new[3]))

# Agrega etiquetas y título al gráfico
#plt.xlabel('α(°)')
#plt.ylabel('Cl')
#plt.title('Cl vs α for Different Reynolds Numbers')

# Agrega una leyenda
#plt.legend()

# Muestra el gráfico
#plt.show()


