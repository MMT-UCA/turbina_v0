""" def acel_maxima():

    Beta = 0
    delta_Beta = 0.1
    lim_error = 0.1
    t_fin = Datos.t_fin_acel
    dt = Datos.dt_acel
    Cd = Datos.C_d
    Z = Datos.Z
    x = Datos.x
    C = 0
    C_dt = 0
    Beta_optimo_seed = 0.1
    Beta_optimo = Beta_optimo_seed
    lista_acel:list[map] = []

    for t in range(0, t_fin + dt, dt):
        print('t:', t)

        T = 0
        T_anterior = 0

        #
        Beta = Beta_optimo
        j = 0
        while not T_anterior > T or j > 100: #Aceleración máxima
            T_anterior = T
            C_media = 0.5 * C + 0.5 * C_dt
            T, Q, W = Helice_Module.helice(C,Beta)
            x_dt, a, C_dt, Fd = avion(C,Z,Cd,T,x)
            Beta = Beta + delta_Beta
            #print('Beta, T_anterior, T:', Beta, T_anterior, T)
            j += 1
        #

        Beta_optimo = Beta - 2*delta_Beta
        i = 0
        T = 1
        T_anterior = 0
        while not T_anterior >= T or i > 100: #Beta óptimo
            T_anterior = T
            C_media = 0.5 * C + 0.5 * C_dt
            T, Q, W = Helice_Module.helice(C,Beta_optimo)
            x_dt, a, C_dt, Fd = avion(C,Z,Cd,T,x)
            #print('Beta_optimo, T_anterior, T:', Beta_optimo, T_anterior, T)
            i += 1

        C = C_dt
        x = x_dt
        if T == 0:
            eta = 0
        else:
            eta = C * T/W/2

        lista_acel.append({'t': t,'Beta_opt': Beta_optimo,'x': x,'C': C, 'a': a, 'Fd': Fd, 'T': T, 'W': W, 'eta': eta})

    return lista_acel """

""" #CSV aceleración máxima

def csv_acel_max():

    def crear_csv_acel_max(datos, nombre_archivo):

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            encabezados = ['t', 'Beta_opt', 'x', 'C', 'a', 'Fd', 'T', 'W', 'eta']
            escritor_csv.writerow(encabezados)

            for fila in datos:
                escritor_csv.writerow([fila[key] for key in encabezados])

    datos_acel_max = acel_maxima()

    nombre_archivo = 'resultados_acel_max.csv'
    crear_csv_acel_max(datos_acel_max, nombre_archivo)
    print(f"Se ha creado el archivo CSV '{nombre_archivo}'.")

#-----------------------------------------------------------------#
#PLOT Acel_maxima T, Fd, W
#Sin csv

def plot_amax_T_Fd_W():

    listaa = acel_maxima()

    t = [diccionario['t'] for diccionario in listaa]

    T = [diccionario['T'] for diccionario in listaa]

    Fd = [diccionario['Fd'] for diccionario in listaa]

    W = [diccionario['W'] for diccionario in listaa]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('W', color='black')
    ax1.plot(t, W, color='green', linestyle='--', label='W')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.set_ylabel('T y Fd', color='black')
    ax2.plot(t, T, color='blue', linestyle='--', label='T')
    ax2.plot(t, Fd, color='red', linestyle='-.', label='Fd')
    ax2.tick_params(axis='y', labelcolor='black')

    plt.title('T, Fd, W')

    fig.legend(loc="upper right")

    fig.tight_layout()

    plt.show()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#Con csv

def plot_amax_T_Fd_W_csv():

    df = pd.read_csv(Datos.resultados_acel_max_csv)
    t = df['t']
    W = df['W']
    T = df['T']
    Fd = df['Fd']

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('W', color='black')
    ax1.plot(t, W, color='green', linestyle='--', label='W')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.set_ylabel('T y Fd', color='black')
    ax2.plot(t, T, color='blue', linestyle='--', label='T')
    ax2.plot(t, Fd, color='red', linestyle='-.', label='Fd')
    ax2.tick_params(axis='y', labelcolor='black')

    plt.title('T, Fd, W')

    fig.legend(loc="upper right")

    fig.tight_layout()

    plt.show()

 """

#Función hélice que arregla el problema de la dispersión de los datos del final pero sólo funciona cuando se llama
#a la función para una lista de valores, por ejemplo un plot, y no cuando sólo se llama para un valor ya que ultimo_T estaría vacío

""" ultimo_T = None
ultimo_Beta = None
def helice(C,Beta):
    global ultimo_T
    global ultimo_Beta

    if Beta >= 50 and C >=200 and ultimo_T == 0 and ultimo_Beta == Beta:
        T = 0 
        Q = 0

    else:

        rhoz = rho(Datos.Z)
        Tempe = Temp(Datos.Z)
        Presi = Pres(Datos.Z) * 1000
        Visc = CP.PropsSI("V", "T", Tempe, "P", Presi, "air")
        Beta_crucero, Beta_n_crucero = Torsion()
        T = 0
        T_anterior = 1 

        j = 0
        #Bucle
        while abs(T - T_anterior) >= 0.1 and j <= 200:
            T_anterior = T
            T = 0
            Q = 0
            i = 0
            r_vind = Datos.r_o
            while r_vind <= (Datos.D)/2:
                Beta_radio = Beta - Beta_n_crucero + Beta_crucero[i]
                Beta_rad = Beta_radio * Datos.pi / 180
                #Call velocidades inducidas 
                Ci, omega_i = velocidades_inducidas(r_vind, T_anterior,Beta_rad,C)
                C_Tcuad = (C + Ci) ** 2 + ((Datos.omega - omega_i) * r_vind) ** 2
                Phi_rad = math.atan((C + Ci) / ((Datos.omega - omega_i) * r_vind))
        
                #Cálculo de beta en cada posición
                alfa_rad = Beta_rad - Phi_rad
                Phi_grad = Phi_rad * 180 / Datos.pi
                alfa = 180 * alfa_rad / Datos.pi
                Re = rhoz * (C_Tcuad) ** 0.5 * Datos.cuerda / Visc
                #####Call Cl_Cd#####
                Cl, Cd = Interpolate_Extrapolate_Module.Interpolate_Extrapolate(alfa, Re)

                #Cálculo de Mach
                A_sonido = CP.PropsSI("A", "T", Tempe, "P", Presi, "air")
                Mach = ((C_Tcuad) ** 0.5) / A_sonido
                #####Call Cl_Cd corregido#####
                Cl_corregido, Cd_corregido, transonico, supersonico = Interpolate_Extrapolate_Module.Cl_Cd_corregido(alfa,Cl,Cd,Mach)

                #Cálculo de tracción y potencia
                dTrac = C_Tcuad * (Cl_corregido * math.cos(Phi_rad) - Cd_corregido * math.sin(Phi_rad)) * Datos.dr
                dQ = C_Tcuad * (Cl_corregido * math.sin(Phi_rad) + Cd_corregido * math.cos(Phi_rad)) * r_vind * Datos.dr
                T = T + dTrac
                Q = Q + dQ

                i += 1
                r_vind += Datos.dr
            T = Datos.Palas * 0.5 * Datos.cuerda * rhoz * T
            Q = Datos.Palas * 0.5 * Datos.cuerda * rhoz * Q
            j += 1 
        if j > 200:
            if T - T_anterior <=300:
                T = (T + T_anterior)/2
                Q = Q
            else:
                T = 0
                Q = 0
    

        if T < 0:
            T = 0
            Q = 0

    W = Q * Datos.omega

    ultimo_T = T
    ultimo_Beta = Beta

    return  T, Q, W """