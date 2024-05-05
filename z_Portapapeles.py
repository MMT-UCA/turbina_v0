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