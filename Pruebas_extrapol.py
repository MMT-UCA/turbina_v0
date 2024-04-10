#IMPORTS

import pandas as pd
import matplotlib.pyplot as plt
import Extrapolate_Module
import Interpolate_Module
import Datos

#-----------------------------------------------------------------#

def Interpolate_Extrapolate_Re(alpha,Re):
    # Re listado

    df_airfoil = pd.read_csv(Datos.archivo_csv)

    if Re == 50000:
        df = pd.read_csv(Datos.url_Re50000, skiprows=10)
    if Re == 100000:
        df = pd.read_csv(Datos.url_Re100000, skiprows=10)
    if Re == 200000:
        df = pd.read_csv(Datos.url_Re200000, skiprows=10)
    if Re == 500000:
        df = pd.read_csv(Datos.url_Re500000, skiprows=10)
    if Re == 1000000:
        df = pd.read_csv(Datos.url_Re1000000, skiprows=10)

    alpha_column = df['Alpha']
    alpha_min_tab = alpha_column.iloc[1]
    alpha_max_tab = alpha_column.iloc[-1]
    # Verificar si el alpha está presente en los datos de Cl y alpha para el Re dado
    if alpha in alpha_column.values:
        # Obtener el índice del valor de alpha en la columna
        idx = alpha_column[alpha_column == alpha].index[0]
        # Obtener el valor correspondiente de Cl
        Cl = df.loc[idx, 'Cl']
        Cd = df.loc[idx, 'Cd']
        return  Cl, Cd # Devolver el dato exacto
    if alpha_min_tab < alpha < alpha_max_tab:
        # Alpha dentro de los límites, realizar interpolación
        Cl = Interpolate_Module.interpolate_Cl(alpha,Re)
        Cd = Interpolate_Module.interpolate_Cd(alpha,Re)
        return Cl, Cd
    else:
        # Alpha fuera de los límites, realizar extrapolación
        simetria = Extrapolate_Module.symmetry(df_airfoil)
        if simetria == True:
            Cl, Cd = Extrapolate_Module.extrapolate_symmetrical(df,df_airfoil,alpha,Re)
        else:
            Cl, Cd = Extrapolate_Module.extrapolate_asymmetrical(df,df_airfoil,alpha,Re)
        return Cl, Cd
    


#-----------------------------------------------------------------#

def Interpolate_Extrapolate(alpha,Re):

    df_airfoil = pd.read_csv(Datos.archivo_csv)

    if Re in [50000, 100000, 200000, 500000, 1000000]:
        Cl, Cd = Interpolate_Extrapolate_Re(alpha,Re)
    else: #Re ≠ [50000, 100000, 200000, 500000, 1000000]
        if 50000 < Re < 1000000:
            Cl = Interpolate_Module.interpolate_Cl(alpha,Re)
            Cd = Interpolate_Module.interpolate_Cd(alpha,Re)
        if 50000 > Re:
            df = pd.read_csv(Datos.url_Re50000, skiprows=10)
            alpha_column = df['Alpha']
            alpha_min_tab = alpha_column.iloc[1]
            alpha_max_tab = alpha_column.iloc[-1]
            simetria = Extrapolate_Module.symmetry(df_airfoil)
            if simetria == True:
                if alpha_min_tab < alpha < alpha_max_tab: 
                    Cl, Cd = Interpolate_Extrapolate_Re(alpha, 50000)
                else:
                    Cl, Cd = Extrapolate_Module.extrapolate_symmetrical(df,df_airfoil,alpha,Re)
            else:
                if alpha_min_tab < alpha < alpha_max_tab: 
                    Cl, Cd = Interpolate_Extrapolate_Re(alpha, 50000)
                else:
                    Cl, Cd = Extrapolate_Module.extrapolate_asymmetrical(df,df_airfoil,alpha,Re)
        if 1000000 < Re:
            df = pd.read_csv(Datos.url_Re1000000, skiprows=10)
            alpha_column = df['Alpha']
            alpha_min_tab = alpha_column.iloc[1]
            alpha_max_tab = alpha_column.iloc[-1]
            simetria = Extrapolate_Module.symmetry(df_airfoil)
            if simetria == True:
                if alpha_min_tab < alpha < alpha_max_tab: 
                    Cl, Cd = Interpolate_Extrapolate_Re(alpha, 1000000)
                else:
                    Cl, Cd = Extrapolate_Module.extrapolate_symmetrical(df,df_airfoil,alpha,Re)
            else:
                if alpha_min_tab < alpha < alpha_max_tab: 
                    Cl, Cd = Interpolate_Extrapolate_Re(alpha, 1000000)
                else:
                    Cl, Cd = Extrapolate_Module.extrapolate_asymmetrical(df,df_airfoil,alpha,Re)
    return Cl, Cd

#-----------------------------------------------------------------#

Cl, Cd = Interpolate_Extrapolate(-7.47,40000)

print('Cl,Cd:',Cl, Cd)

#-----------------------------------------------------------------#

#PLOT

valores_Cl = []
valores_Cd = []
valores_alpha = []
Re = 2000002

for alpha in range(-180, 180):
    # Llama a tu función para calcular Cl y Cd
    Cl, Cd = Interpolate_Extrapolate(alpha,Re)
    # Agrega los valores a las listas correspondientes
    valores_Cl.append(Cl)
    valores_Cd.append(Cd)
    valores_alpha.append(alpha)

plt.scatter(valores_alpha, valores_Cl, color='red')

# Agrega etiquetas y título al gráfico
plt.xlabel('α(°)')
plt.ylabel('Cl')
plt.title('Cl vs α')

# Agrega una leyenda
#plt.legend()

# Muestra el gráfico
plt.show()

