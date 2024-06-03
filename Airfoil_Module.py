#-----------------------------------------------------------------#
#MÓDULO PERFIL VARIABLE
#Cálculos de perfil variable
#-----------------------------------------------------------------#
#IMPORTS
import math
import pandas as pd
import matplotlib.pyplot as plt
import Datos
import numpy as np
#-----------------------------------------------------------------#
#Función de cálculo de coordenadas del perfil intermedio

#Esta función lee en Datos si el perfil es variable o fijo. Si es fijo lee el archivo de datos del perfil asignado.
#Si es variable lee las coordenadas del perfil para cada radio. Si el valor del radio tiene un perfil asignado, 
#se leerá su archivo de coordenadas .csv. Si el radio no tiene un perfil asignado,
#se realizará una interpolación entre las coordenadas de los perfiles anterior y posterior.
#Las coordenadas del perfil se calculan para el punto medio posterior a r (r_puntomedio).

def coordenadas_perfil(r,perfil_variable):

    if perfil_variable == False:

        archivo = Datos.archivo_csv
        df_airfoil = pd.read_csv(archivo)
    
    else:

        df = pd.read_csv(Datos.archivo_csv_variable)
        radio = df['radio']
        perfil = df['perfil']
        nombre_archivo = df['nombre_archivo']
        tol = 0.05

        x_intra_extra = []
        y_intra = []
        y_extra = []

        r_puntomedio = r + (Datos.dr / 2)

        if np.isclose(r_puntomedio, radio).any():
            # Encontrar el índice del valor cercano
            idx = np.where(np.isclose(radio, r_puntomedio))[0][0]
            fila_actual = df.iloc[idx]
            nombre_coordenadas = fila_actual['nombre_archivo']
            df_airfoil = pd.read_csv(nombre_coordenadas + '.csv')

        else:
            # Encontrar el valor inmediatamente superior en la lista
            r_upper = radio[radio >= r_puntomedio].min()
            # Encontrar el valor inmediatamente inferior en la lista
            r_lower = radio[radio <= r_puntomedio].max()
            # Obtener los valores de perfil correspondientes a los r encontrados
            perfil_lower = nombre_archivo[radio == r_lower].iloc[0] if not pd.isnull(r_lower) else None
            perfil_upper = nombre_archivo[radio == r_upper].iloc[0] if not pd.isnull(r_upper) else None
            df_airfoil_lower = pd.read_csv(perfil_lower + '.csv')
            df_airfoil_upper = pd.read_csv(perfil_upper + '.csv')

            x_lower_list = df_airfoil_lower['x'].tolist()
            y_lower_list = df_airfoil_lower['y'].tolist()

            x_upper_list = df_airfoil_upper['x'].tolist()
            y_upper_list = df_airfoil_upper['y'].tolist()

            # Separar valores positivos y negativos
            x_pos_lower, y_pos_lower = zip(*[(x, y) for x, y in zip(x_lower_list, y_lower_list) if y >= 0])
            x_neg_lower, y_neg_lower = zip(*[(x, y) for x, y in zip(x_lower_list, y_lower_list) if y <= 0])

            x_pos_upper, y_pos_upper = zip(*[(x, y) for x, y in zip(x_upper_list, y_upper_list) if y >= 0])
            x_neg_upper, y_neg_upper = zip(*[(x, y) for x, y in zip(x_upper_list, y_upper_list) if y <= 0])


            x = 0
            while x <= 1.0005:

                if x == 0:
                    y_lower_lower_int = 0
                    y_upper_lower_int = 0
                    y_lower_upper_int = 0
                    y_upper_upper_int = 0
                    y_lower_lower_ext = 0
                    y_upper_lower_ext = 0
                    y_lower_upper_ext = 0
                    y_upper_upper_ext = 0

                    x_lower_lower_int = 0
                    x_upper_lower_int = 0
                    x_lower_upper_int = 0
                    x_upper_upper_int = 0
                    x_lower_lower_ext = 0
                    x_upper_lower_ext = 0
                    x_lower_upper_ext = 0
                    x_upper_upper_ext = 0

                elif 1e-20 <= x <= 1.0005:
                    x_lower_lower_int = max([x_max for x_max in x_neg_lower if x_max <= x])
                    y_lower_lower_int = y_neg_lower[x_neg_lower.index(x_lower_lower_int)]
                    x_lower_upper_int = max([x_max for x_max in x_neg_upper if x_max <= x])
                    y_lower_upper_int = y_neg_upper[x_neg_upper.index(x_lower_upper_int)]
                    x_lower_lower_ext = max([x_max for x_max in x_pos_lower if x_max <= x])
                    y_lower_lower_ext = y_pos_lower[x_pos_lower.index(x_lower_lower_ext)]
                    x_lower_upper_ext = max([x_max for x_max in x_pos_upper if x_max <= x])
                    y_lower_upper_ext = y_pos_upper[x_pos_upper.index(x_lower_upper_ext)]
                    
                    x_upper_lower_int = x_lower_lower_int 
                    y_upper_lower_int = y_lower_lower_int 
                    x_upper_upper_int = x_lower_upper_int 
                    y_upper_upper_int = y_lower_upper_int
                    x_upper_lower_ext = x_lower_lower_ext 
                    y_upper_lower_ext = y_lower_lower_ext
                    x_upper_upper_ext = x_lower_upper_ext
                    y_upper_upper_ext = y_lower_upper_ext 


                else:

                    #Intradós
                    #Lista lower
                    #Encontrar el valor inmediatamente superior en la lista
                    x_upper_lower_int = min([x_min for x_min in x_neg_lower if x_min >= x])
                    # Encontrar el valor inmediatamente inferior en la lista
                    x_lower_lower_int = max([x_max for x_max in x_neg_lower if x_max <= x])
                    # Obtener los valores de y correspondientes a los x encontrados
                    y_lower_lower_int = y_neg_lower[x_neg_lower.index(x_lower_lower_int)]
                    y_upper_lower_int = y_neg_lower[x_neg_lower.index(x_upper_lower_int)]

                    #Lista upper
                    #Encontrar el valor inmediatamente superior en la lista
                    x_upper_upper_int = min([x_min for x_min in x_neg_upper if x_min >= x])
                    # Encontrar el valor inmediatamente inferior en la lista
                    x_lower_upper_int = max([x_max for x_max in x_neg_upper if x_max <= x])
                    # Obtener los valores de y correspondientes a los x encontrados
                    y_lower_upper_int = y_neg_upper[x_neg_upper.index(x_lower_upper_int)]
                    y_upper_upper_int = y_neg_upper[x_neg_upper.index(x_upper_upper_int)]
        

                    #Extradós
                    #Lista lower
                    #Encontrar el valor inmediatamente superior en la lista
                    x_upper_lower_ext = min([x_min for x_min in x_pos_lower if x_min >= x])
                    # Encontrar el valor inmediatamente inferior en la lista
                    x_lower_lower_ext = max([x_max for x_max in x_pos_lower if x_max <= x])
                    # Obtener los valores de y correspondientes a los x encontrados
                    y_lower_lower_ext = y_pos_lower[x_pos_lower.index(x_lower_lower_ext)]
                    y_upper_lower_ext = y_pos_lower[x_pos_lower.index(x_upper_lower_ext)]

                    #Lista upper
                    #Encontrar el valor inmediatamente superior en la lista
                    x_upper_upper_ext = min([x_min for x_min in x_pos_upper if x_min >= x])
                    # Encontrar el valor inmediatamente inferior en la lista
                    x_lower_upper_ext = max([x_max for x_max in x_pos_upper if x_max <= x])
                    # Obtener los valores de y correspondientes a los x encontrados
                    y_lower_upper_ext = y_pos_upper[x_pos_upper.index(x_lower_upper_ext)]
                    y_upper_upper_ext = y_pos_upper[x_pos_upper.index(x_upper_upper_ext)]
                    

                def interpolate_coordinates(x,x_lower,x_upper,y_lower,y_upper):

                    if x_lower == 0 and x_upper == 0:
                        y_airfoil = 0
                    elif x_lower == x_upper and y_lower == y_upper:
                        y_airfoil = y_upper
                    else:
                        y_airfoil = y_lower + (y_upper-y_lower)*((x-x_lower)/(x_upper-x_lower))

                    return y_airfoil
                
                y_airfoil_anterior_intra = interpolate_coordinates(x,x_lower_lower_int,x_upper_lower_int,y_lower_lower_int,y_upper_lower_int)
                y_airfoil_anterior_extra = interpolate_coordinates(x,x_lower_lower_ext,x_upper_lower_ext,y_lower_lower_ext,y_upper_lower_ext)
                y_airfoil_posterior_intra = interpolate_coordinates(x,x_lower_upper_int,x_upper_upper_int,y_lower_upper_int,y_upper_upper_int)
                y_airfoil_posterior_extra = interpolate_coordinates(x,x_lower_upper_ext,x_upper_upper_ext,y_lower_upper_ext,y_upper_upper_ext)
                
                def interpolate_airfoil(r,r_lower,r_upper,y_airfoil_anterior,y_airfoil_posterior):
                    
                    y_coordinate = y_airfoil_anterior + (y_airfoil_posterior-y_airfoil_anterior)*((r-r_lower)/(r_upper-r_lower))

                    return y_coordinate
                
                y_coordinate_intra = interpolate_coordinates(r_puntomedio,r_lower,r_upper,y_airfoil_anterior_intra,y_airfoil_posterior_intra)
                y_coordinate_extra = interpolate_coordinates(r_puntomedio,r_lower,r_upper,y_airfoil_anterior_extra,y_airfoil_posterior_extra)
                    
                x_intra_extra.append(x)
                y_intra.append(y_coordinate_intra)
                y_extra.append(y_coordinate_extra)

                x += tol

            # Crear la lista x deseada
            x_list = x_intra_extra[::-1][1:] + x_intra_extra[1:]

            # Crear la lista y deseada
            y_list = y_extra[::-1][1:] + y_intra[1:]

            data = {'x': x_list, 'y': y_list}
            df_airfoil = pd.DataFrame(data)
    
    return df_airfoil

#-----------------------------------------------------------------#
#Función para graficar el perfil intermedio calculado

def plot_intermediate_airfoil():

    r = 0.25
    perfil = True

    df_resultado = coordenadas_perfil(r, perfil)
    print(df_resultado['x'])
    df_airfoil_lower = pd.read_csv('Coordenadas_NACA0012.csv')
    df_airfoil_upper = pd.read_csv('Coordenadas_NACA2414.csv')

    plt.figure(figsize=(10, 5))
    plt.scatter(df_airfoil_lower['x'], df_airfoil_lower['y'], color='red', label='NACA0012', marker='o')
    plt.scatter(df_airfoil_upper['x'], df_airfoil_upper['y'], color='green', label='NACA2414', marker='o')
    plt.scatter(df_resultado['x'], df_resultado['y'],color='blue', marker='o', linestyle='-')

    plt.title('Interpolación de Perfil de Coordenadas')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()

#-----------------------------------------------------------------#

#Esta función lee en Datos si el perfil es variable o fijo. Si es fijo lee los archivos de datos para diferentes Re del apartado perfil fijo.
#Si es variable lee las coordenadas del perfil para cada radio. Si el valor del radio tiene un perfil asignado, 
#se leerá su archivo de coordenadas .csv. Si el radio no tiene un perfil asignado,
#se realizará una interpolación entre las coordenadas de los perfiles anterior y posterior.

def archivo_Re(r,perfil_variable,Re):

    if perfil_variable == False:
        
        nombre_archivo_Re = 'Datos.url_Re' + str(Re)
        archivo_Re = eval(nombre_archivo_Re)
        df_Re = pd.read_csv(archivo_Re)
    
    else:

        df = pd.read_csv(Datos.archivo_csv_variable)
        radio = df['radio']
        perfil = df['perfil']
        nombre_archivo = df['nombre_archivo']
        tol = 0.1

        
        alpha_list = []
        Cl_list= []
        Cd_list = [] 

        r_puntomedio = r + (Datos.dr / 2)

        if np.isclose(r_puntomedio, radio).any():
            # Encontrar el índice del valor cercano
            idx = np.where(np.isclose(radio, r_puntomedio))[0][0]
            fila_actual = df.iloc[idx]
            nombre_perfil = fila_actual['perfil']
            nombre_archivo_Re = 'Datos.url__' + nombre_perfil + '_Re' + str(Re)
            archivo_Re = eval(nombre_archivo_Re)
            df_Re = pd.read_csv(archivo_Re,skiprows=10)

        else:
            # Encontrar el valor inmediatamente superior en la lista
            r_upper = radio[radio >= r_puntomedio].min()
            # Encontrar el valor inmediatamente inferior en la lista
            r_lower = radio[radio <= r_puntomedio].max()
            # Obtener los valores de perfil correspondientes a los r encontrados
            perfil_lower = perfil[radio == r_lower].iloc[0] if not pd.isnull(r_lower) else None
            perfil_upper = perfil[radio == r_upper].iloc[0] if not pd.isnull(r_upper) else None
            nombre_archivo_Re_lower = 'Datos.url__' + perfil_lower + '_Re' + str(Re)
            archivo_Re_lower = eval(nombre_archivo_Re_lower)
            df_airfoil_lower = pd.read_csv(archivo_Re_lower, skiprows=10)
            nombre_archivo_Re_upper = 'Datos.url__' + perfil_upper + '_Re' + str(Re)
            archivo_Re_upper = eval(nombre_archivo_Re_upper)
            df_airfoil_upper = pd.read_csv(archivo_Re_upper, skiprows=10)

            alpha_column_lower = df_airfoil_lower['Alpha']
            alpha_min_tab_lower = alpha_column_lower.iloc[1]
            alpha_max_tab_lower = alpha_column_lower.iloc[-1]
            alpha_column_upper = df_airfoil_upper['Alpha']
            alpha_min_tab_upper = alpha_column_upper.iloc[1]
            alpha_max_tab_upper = alpha_column_upper.iloc[-1]

            if alpha_min_tab_lower < alpha_min_tab_upper or alpha_min_tab_lower == alpha_min_tab_upper:
                alpha_min_tab = alpha_min_tab_upper
            else:
                alpha_min_tab = alpha_min_tab_lower

            if alpha_max_tab_lower < alpha_max_tab_upper or alpha_max_tab_lower == alpha_max_tab_upper:
                alpha_max_tab = alpha_max_tab_lower
            else:
                alpha_max_tab = alpha_max_tab_upper

            alpha_lower_list = df_airfoil_lower['Alpha'].tolist()
            Cl_lower_list = df_airfoil_lower['Cl'].tolist()
            Cd_lower_list = df_airfoil_lower['Cd'].tolist()

            alpha_upper_list = df_airfoil_upper['Alpha'].tolist()
            Cl_upper_list = df_airfoil_upper['Cl'].tolist()
            Cd_upper_list = df_airfoil_upper['Cd'].tolist()

            alpha = alpha_min_tab
            while alpha <= alpha_max_tab:

                #Lista lower
                #Encontrar el valor inmediatamente superior en la lista
                alpha_upper_lower = min([alpha_min for alpha_min in alpha_lower_list if alpha_min >= alpha])
                # Encontrar el valor inmediatamente inferior en la lista
                alpha_lower_lower = max([alpha_max for alpha_max in alpha_lower_list if alpha_max <= alpha])
                # Obtener los valores de Cl correspondientes a los alpha encontrados
                Cl_lower_lower = Cl_lower_list[alpha_lower_list.index(alpha_lower_lower)]
                Cl_upper_lower = Cl_lower_list[alpha_lower_list.index(alpha_upper_lower)]
                # Obtener los valores de Cd correspondientes a los alpha encontrados
                Cd_lower_lower = Cd_lower_list[alpha_lower_list.index(alpha_lower_lower)]
                Cd_upper_lower = Cd_lower_list[alpha_lower_list.index(alpha_upper_lower)]

                #Lista upper
                #Encontrar el valor inmediatamente superior en la lista
                alpha_upper_upper = min([alpha_min for alpha_min in alpha_upper_list if alpha_min >= alpha])
                # Encontrar el valor inmediatamente inferior en la lista
                alpha_lower_upper = max([alpha_max for alpha_max in alpha_upper_list if alpha_max <= alpha])
                # Obtener los valores de Cl correspondientes a los alpha encontrados
                Cl_lower_upper = Cl_upper_list[alpha_upper_list.index(alpha_lower_upper)]
                Cl_upper_upper = Cl_upper_list[alpha_upper_list.index(alpha_upper_upper)]
                # Obtener los valores de Cd correspondientes a los alpha encontrados
                Cd_lower_upper = Cd_upper_list[alpha_upper_list.index(alpha_lower_upper)]
                Cd_upper_upper = Cd_upper_list[alpha_upper_list.index(alpha_upper_upper)]
        
                def interpolate_Cl_Cd(alpha,alpha_lower,alpha_upper,C_lower,C_upper):

                    if alpha_lower == alpha_upper and C_lower == C_upper:
                        C = C_upper
                    else:
                        C = C_lower + (C_upper-C_lower)*((alpha-alpha_lower)/(alpha_upper-alpha_lower))

                    return C
                
                Cl_lower_airfoil = interpolate_Cl_Cd(alpha,alpha_lower_lower,alpha_upper_lower,Cl_lower_lower,Cl_upper_lower)
                Cl_upper_airfoil = interpolate_Cl_Cd(alpha,alpha_lower_upper,alpha_upper_upper,Cl_lower_upper,Cl_upper_upper)
                Cd_lower_airfoil = interpolate_Cl_Cd(alpha,alpha_lower_lower,alpha_upper_lower,Cd_lower_lower,Cd_upper_lower)
                Cd_upper_airfoil = interpolate_Cl_Cd(alpha,alpha_lower_upper,alpha_upper_upper,Cd_lower_upper,Cd_upper_upper)

                def interpolate_final(r,r_lower,r_upper,C_airfoil_anterior,C_airfoil_posterior):
                    
                    C_final = C_airfoil_anterior + (C_airfoil_posterior-C_airfoil_anterior)*((r-r_lower)/(r_upper-r_lower))

                    return C_final
                
                Cl_final = interpolate_final(r_puntomedio,r_lower,r_upper,Cl_lower_airfoil,Cl_upper_airfoil)
                Cd_final = interpolate_final(r_puntomedio,r_lower,r_upper,Cd_lower_airfoil,Cd_upper_airfoil)
                    
                alpha_list.append(alpha)
                Cl_list.append(Cl_final)
                Cd_list.append(Cd_final)

                alpha += tol


            data = {'Alpha': alpha_list, 'Cl': Cl_list, 'Cd': Cd_list}
            df_Re = pd.DataFrame(data)
    
    return df_Re

#-----------------------------------------------------------------#
#PRUEBAS
""" r = 0.25
perfil = True
Re = 50000
archivo_Re(r,perfil,Re) """