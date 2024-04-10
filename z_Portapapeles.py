If alfa_dato(ind_Re - 1, 1) > alfa Then 'alfa fuera de rango. es menor que el mínimo tabulado
    
            'Extrapolación de la polar de Lorenzo Battisti et al https://doi.org/10.1016/j.renene.2020.03.150
                    
            alfa_min = alfa_dato(ind_Re - 1, 1) 'Selecciona el alfa de separación
            Cl_min = Cl_dato(ind_Re - 1, 1)
            Cd_min = Cd_dato(ind_Re - 1, 1)
            
            'Cálculo de parámetros para el modelo de Lorenzo Battisti
            Cd_90 = 1.98 - 0.64 * (1 / 2 * (t_c) ^ 2) - 0.44 * t_c + 1.39 * h_c
            'Cd_270 = 1.98 - 0.64 * (1 / 2 * (t_c) ^ 2) - 0.44 * t_c - 1.39 * h_c
            'beta_prim = alfa - alfazero(ind_Re - 1) * Cos(alfa * Pi / 180)
              
            'Cd_func = (Cd_90 + Cd_270) / 2 + ((Cd_90 - Cd_270) / 2) * Sin(beta_prim * Pi / 180)
            Log10 = Log(Re_numero(ind_Re - 1)) / Log(10)
            CDf = (0.455 / (Log10 ^ 2.58)) - 1700 / Re_numero(ind_Re - 1)
                 
            'Cálculo del coeficiente de la normal y de la tangencial de la Polar
            CN = (Cd_90) * ((Sin(alfa * Pi / 180)) + 0.0023 * (Sin(2 * alfa * Pi / 180)) / (0.38 + (0.62 * Abs((Sin(alfa * Pi / 180)))) + (3.7 * t_c * ((Cos(alfa * Pi / 180)) ^ 8))))
            CT = (Cd_90) * 0.3 * t_c * (Abs(Sin(alfa * Pi / 180) + 0.1 * Sin(2 * alfa * Pi / 180))) * (1 - 2 * Cos(alfa * Pi / 180)) - CDf * Cos(alfa * Pi / 180)
            
            'Cálculo de los coeficientes de sustentación y arrastre
            Cl_1 = CN * Cos(alfa * Pi / 180) + CT * Sin(alfa * Pi / 180)
            Cd_1 = (CN * Sin(alfa * Pi / 180) - CT * Cos(alfa * Pi / 180)) * (1 - 0.4 * (1 - Exp(-(11.4) / (AR / (Sin(alfa * Pi / 180))))))
        
            'En caso de que alfa esté entre el de desprendimiento (alfa_min) y el de separación (-45)
            If alfa >= -45 And alfa <= alfa_min Then
            
                'Cálculo de los coeficientes de desprendimiento
                CT_ds_menos = ((Cl_min / Cos(alfa_min * Pi / 180)) - (Cd_min / Sin(alfa_min * Pi / 180))) / ((Sin(alfa_min * Pi / 180) / Cos(alfa_min * Pi / 180)) + (Cos(alfa_min * Pi / 180) / Sin(alfa_min * Pi / 180)))
                CN_ds_menos = (Cl_min - (CT_ds_menos * Sin(alfa_min * Pi / 180))) / (Cos(alfa_min * Pi / 180))
                f_menos = ((alfa + 45) / (alfa_min + 45)) ^ 2
                
                'Cálculo de los coeficientes de separación
                'beta_prim = -45 - alfazero(ind_Re - 1) * Cos(-45 * Pi / 180)
                'Cd_func = (Cd_90 + Cd_270) / 2 + ((Cd_90 - Cd_270) / 2) * Sin(beta_prim * Pi / 180)
                Log10 = Log(Re_numero(ind_Re - 1)) / Log(10)
                CDf = (0.455 / (Log10 ^ 2.58)) - 1700 / Re_numero(ind_Re - 1)
                
                CN_SEP = (Cd_90) * ((Sin(-45 * Pi / 180)) + 0.0023 * (Sin(2 * -45 * Pi / 180)) / (0.38 + (0.62 * Abs((Sin(-45 * Pi / 180)))) + (3.7 * t_c * ((Cos(-45 * Pi / 180)) ^ 8))))
                CT_SEP = (Cd_90) * 0.3 * t_c * (Abs(Sin(-45 * Pi / 180) + 0.1 * Sin(2 * -45 * Pi / 180))) * (1 - 2 * Cos(-45 * Pi / 180)) - CDf * Cos(-45 * Pi / 180)
                
                'Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
                CN_menos = CN_ds_menos * f_menos + CN_SEP * (1 - f_menos)
                CT_menos = CT_ds_menos * f_menos + CT_SEP * (1 - f_menos)
                
                'Cálculo de los coeficientes de sustentación y arrastre
                Cl_1 = CN_menos * Cos(alfa * Pi / 180) + CT_menos * Sin(alfa * Pi / 180)
                Cd_1 = (CN_menos * Sin(alfa * Pi / 180) - CT_menos * Cos(alfa * Pi / 180)) * (1 - 0.4 * (1 - Exp(-(11.4) / (AR / (Sin(alfa * Pi / 180))))))
            End If










alpha_column = df['Alpha']
    alpha_min_tab = alpha_column.iloc[1]
    alpha_max_tab = alpha_column.iloc[-1]
    Cl_column = df['Cl']
    Cl_min_tab = Cl_column.iloc[1]
    Cl_max_tab = Cl_column.iloc[-1]
    Cd_column = df['Cd']
    Cd_min_tab = Cd_column.iloc[1]
    Cd_max_tab = Cd_column.iloc[-1]

    t_c = Camber_Module.thickness_max(df_airfoil)
    h_c = Camber_Module.camber_max(df_airfoil)

    #Cl_1,Cd_1
    if alpha < alpha_min_tab : #alpha menor que el mínimo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_90) * ((math.sin(alpha * Datos.pi / 180)) + 0.0023 * (math.sin(2 * alpha * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_90) * 0.3 * t_c * (abs(math.sin(alpha * Datos.pi / 180) + 0.1 * math.sin(2 * alpha * Datos.pi / 180))) * (1 - 2 * math.cos(alpha * Datos.pi / 180)) - CD_f * math.cos(alpha * Datos.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl_1 = CN * math.cos(alpha * Datos.pi / 180) + CT * math.sin(alpha * Datos.pi / 180)
        Cd_1 = (CN * math.sin(alpha * Datos.pi / 180) - CT * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
        if alpha >= -45 and alpha <= alpha_min_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_menos = ((Cl_min_tab / math.cos(alpha_min_tab * Datos.pi / 180)) - (Cd_min_tab / math.sin(alpha_min_tab * Datos.pi / 180))) / ((math.sin(alpha_min_tab * Datos.pi / 180) / math.cos(alpha_min_tab * Datos.pi / 180)) + (math.cos(alpha_min_tab * Datos.pi / 180) / math.sin(alpha_min_tab * Datos.pi / 180)))
            CN_ds_menos = (Cl_min_tab - (CT_ds_menos * math.sin(alpha_min_tab * Datos.pi / 180))) / (math.cos(alpha_min_tab * math.pi / 180))
            f_menos = ((alpha + 45) / (alpha_min_tab + 45)) ** 2
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_90) * ((math.sin(-45 * Datos.pi / 180)) + 0.0023 * (math.sin(2 * -45 * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(-45 * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(-45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_90) * 0.3 * t_c * (abs(math.sin(-45 * Datos.pi / 180) + 0.1 * math.sin(2 * -45 * Datos.pi / 180))) * (1 - 2 * math.cos(-45 * Datos.pi / 180)) - CD_f * math.cos(-45 * Datos.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_menos = CN_ds_menos * f_menos + CN_sep * (1 - f_menos)
            CT_menos = CT_ds_menos * f_menos + CT_sep * (1 - f_menos)
            #Coeficientes de sustentación y resistencia
            Cl_1 = CN_menos * math.cos(alpha * Datos.pi / 180) + CT_menos * math.sin(alpha * Datos.pi / 180)
            Cd_1 = (CN_menos * math.sin(alpha * Datos.pi / 180) - CT_menos * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
            
    else:  #alpha mayor que el máximo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_90) * ((math.sin(alpha * Datos.pi / 180)) + 0.0023 * (math.sin(2 * alpha * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_90) * 0.3 * t_c * (abs(math.sin(alpha * Datos.pi / 180) + 0.1 * math.sin(2 * alpha * Datos.pi / 180))) * (1 - 2 * math.cos(alpha * Datos.pi / 180)) - CD_f * math.cos(alpha * Datos.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl_1 = CN * math.cos(alpha * Datos.pi / 180) + CT * math.sin(alpha * Datos.pi / 180)
        Cd_1 = (CN * math.sin(alpha * Datos.pi / 180) - CT * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
        if alpha <= 45 and alpha >= alpha_max_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_mas = ((Cl_max_tab / math.cos(alpha_max_tab * Datos.pi / 180)) - (Cd_max_tab / math.sin(alpha_max_tab * Datos.pi / 180))) / ((math.sin(alpha_max_tab * Datos.pi / 180) / math.cos(alpha_max_tab * Datos.pi / 180)) + (math.cos(alpha_max_tab * Datos.pi / 180) / math.sin(alpha_max_tab * Datos.pi / 180)))
            CN_ds_mas = (Cl_max_tab - (CT_ds_mas * math.sin(alpha_max_tab * Datos.pi / 180))) / (math.cos(alpha_max_tab * math.pi / 180))
            f_mas = ((alpha - 45) / (alpha_max_tab - 45)) ** 2
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_90) * ((math.sin(45 * Datos.pi / 180)) + 0.0023 * (math.sin(2 * 45 * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(45 * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_90) * 0.3 * t_c * (abs(math.sin(45 * Datos.pi / 180) + 0.1 * math.sin(2 * 45 * Datos.pi / 180))) * (1 - 2 * math.cos(45 * Datos.pi / 180)) - CD_f * math.cos(45 * Datos.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_mas = CN_ds_mas * f_mas + CN_sep * (1 - f_mas)
            CT_mas = CT_ds_mas * f_mas + CT_sep * (1 - f_mas)
            #Coeficientes de sustentación y resistencia
            Cl_1 = CN_mas * math.cos(alpha * Datos.pi / 180) + CT_mas * math.sin(alpha * Datos.pi / 180)
            Cd_1 = (CN_mas * math.sin(alpha * Datos.pi / 180) - CT_mas * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
    
    #Cl_2,Cd_2
    if alpha < alpha_min_tab : #alpha menor que el mínimo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_90) * ((math.sin(alpha * Datos.pi / 180)) + 0.0023 * (math.sin(2 * alpha * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_90) * 0.3 * t_c * (abs(math.sin(alpha * Datos.pi / 180) + 0.1 * math.sin(2 * alpha * Datos.pi / 180))) * (1 - 2 * math.cos(alpha * Datos.pi / 180)) - CD_f * math.cos(alpha * Datos.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl_2 = CN * math.cos(alpha * Datos.pi / 180) + CT * math.sin(alpha * Datos.pi / 180)
        Cd_2 = (CN * math.sin(alpha * Datos.pi / 180) - CT * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
        if alpha >= -45 and alpha <= alpha_min_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_menos = ((Cl_min_tab / math.cos(alpha_min_tab * Datos.pi / 180)) - (Cd_min_tab / math.sin(alpha_min_tab * Datos.pi / 180))) / ((math.sin(alpha_min_tab * Datos.pi / 180) / math.cos(alpha_min_tab * Datos.pi / 180)) + (math.cos(alpha_min_tab * Datos.pi / 180) / math.sin(alpha_min_tab * Datos.pi / 180)))
            CN_ds_menos = (Cl_min_tab - (CT_ds_menos * math.sin(alpha_min_tab * Datos.pi / 180))) / (math.cos(alpha_min_tab * math.pi / 180))
            f_menos = ((alpha + 45) / (alpha_min_tab + 45)) ** 2
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_90) * ((math.sin(-45 * Datos.pi / 180)) + 0.0023 * (math.sin(2 * -45 * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(-45 * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(-45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_90) * 0.3 * t_c * (abs(math.sin(-45 * Datos.pi / 180) + 0.1 * math.sin(2 * -45 * Datos.pi / 180))) * (1 - 2 * math.cos(-45 * Datos.pi / 180)) - CD_f * math.cos(-45 * Datos.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_menos = CN_ds_menos * f_menos + CN_sep * (1 - f_menos)
            CT_menos = CT_ds_menos * f_menos + CT_sep * (1 - f_menos)
            #Coeficientes de sustentación y resistencia
            Cl_2 = CN_menos * math.cos(alpha * Datos.pi / 180) + CT_menos * math.sin(alpha * Datos.pi / 180)
            Cd_2 = (CN_menos * math.sin(alpha * Datos.pi / 180) - CT_menos * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
            
    else:  #alpha mayor que el máximo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_90) * ((math.sin(alpha * Datos.pi / 180)) + 0.0023 * (math.sin(2 * alpha * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_90) * 0.3 * t_c * (abs(math.sin(alpha * Datos.pi / 180) + 0.1 * math.sin(2 * alpha * Datos.pi / 180))) * (1 - 2 * math.cos(alpha * Datos.pi / 180)) - CD_f * math.cos(alpha * Datos.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl_2 = CN * math.cos(alpha * Datos.pi / 180) + CT * math.sin(alpha * Datos.pi / 180)
        Cd_2 = (CN * math.sin(alpha * Datos.pi / 180) - CT * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
        if alpha <= 45 and alpha >= alpha_max_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_mas = ((Cl_max_tab / math.cos(alpha_max_tab * Datos.pi / 180)) - (Cd_max_tab / math.sin(alpha_max_tab * Datos.pi / 180))) / ((math.sin(alpha_max_tab * Datos.pi / 180) / math.cos(alpha_max_tab * Datos.pi / 180)) + (math.cos(alpha_max_tab * Datos.pi / 180) / math.sin(alpha_max_tab * Datos.pi / 180)))
            CN_ds_mas = (Cl_max_tab - (CT_ds_mas * math.sin(alpha_max_tab * Datos.pi / 180))) / (math.cos(alpha_max_tab * math.pi / 180))
            f_mas = ((alpha - 45) / (alpha_max_tab - 45)) ** 2
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_90) * ((math.sin(45 * Datos.pi / 180)) + 0.0023 * (math.sin(2 * 45 * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(45 * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_90) * 0.3 * t_c * (abs(math.sin(45 * Datos.pi / 180) + 0.1 * math.sin(2 * 45 * Datos.pi / 180))) * (1 - 2 * math.cos(45 * Datos.pi / 180)) - CD_f * math.cos(45 * Datos.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_mas = CN_ds_mas * f_mas + CN_sep * (1 - f_mas)
            CT_mas = CT_ds_mas * f_mas + CT_sep * (1 - f_mas)
            #Coeficientes de sustentación y resistencia
            Cl_2 = CN_mas * math.cos(alpha * Datos.pi / 180) + CT_mas * math.sin(alpha * Datos.pi / 180)
            Cd_2 = (CN_mas * math.sin(alpha * Datos.pi / 180) - CT_mas * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
            
    return Cl_1,Cl_2,Cd_1,Cd_2







if alpha < alpha_min_tab : #alpha menor que el mínimo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        CD_270 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c - 1.39 * h_c
        beta_prim = alpha - alphazero * math.cos(alpha * Datos.pi / 180)
        CD_func = (CD_90 + CD_270)/2 + ((CD_90 - CD_270) / 2) * math.sin(beta_prim * Datos.pi / 180)
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_func) * ((math.sin(alpha * Datos.pi / 180)) + 0.0023 * (math.sin(2 * alpha * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_func) * 0.3 * t_c * (abs(math.sin(alpha * Datos.pi / 180) + 0.1 * math.sin(2 * alpha * Datos.pi / 180))) * (1 - 2 * math.cos(alpha * Datos.pi / 180)) - CD_f * math.cos(alpha * Datos.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl = CN * math.cos(alpha * Datos.pi / 180) + CT * math.sin(alpha * Datos.pi / 180)
        Cd = (CN * math.sin(alpha * Datos.pi / 180) - CT * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
        if alpha >= -45 and alpha <= alpha_min_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_menos = ((Cl_min_tab / math.cos(alpha_min_tab * Datos.pi / 180)) - (Cd_min_tab / math.sin(alpha_min_tab * Datos.pi / 180))) / ((math.sin(alpha_min_tab * Datos.pi / 180) / math.cos(alpha_min_tab * Datos.pi / 180)) + (math.cos(alpha_min_tab * Datos.pi / 180) / math.sin(alpha_min_tab * Datos.pi / 180)))
            CN_ds_menos = (Cl_min_tab - (CT_ds_menos * math.sin(alpha_min_tab * Datos.pi / 180))) / (math.cos(alpha_min_tab * math.pi / 180))
            beta_prim = -45 - alphazero * math.cos(-45 * Datos.pi / 180)
            CD_func = (CD_90 + CD_270)/2 + ((CD_90 - CD_270) / 2) * math.sin(beta_prim * Datos.pi / 180)
            f_menos = ((alpha + 45) / (alpha_min_tab + 45)) ** 2
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_func) * ((math.sin(-45 * Datos.pi / 180)) + 0.0023 * (math.sin(2 * -45 * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(-45 * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(-45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_func) * 0.3 * t_c * (abs(math.sin(-45 * Datos.pi / 180) + 0.1 * math.sin(2 * -45 * Datos.pi / 180))) * (1 - 2 * math.cos(-45 * Datos.pi / 180)) - CD_f * math.cos(-45 * Datos.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_menos = CN_ds_menos * f_menos + CN_sep * (1 - f_menos)
            CT_menos = CT_ds_menos * f_menos + CT_sep * (1 - f_menos)
            #Coeficientes de sustentación y resistencia
            Cl = CN_menos * math.cos(alpha * Datos.pi / 180) + CT_menos * math.sin(alpha * Datos.pi / 180)
            Cd = (CN_menos * math.sin(alpha * Datos.pi / 180) - CT_menos * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
            
    else:  #alpha mayor que el máximo tabulado
        #Cálculo de parámetros
        CD_90 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c + 1.39 * h_c
        CD_270 = 1.98 - 0.64 * (0.5 * (t_c)**2) - 0.44 * t_c - 1.39 * h_c
        beta_prim = alpha - alphazero * math.cos(alpha * Datos.pi / 180)
        CD_func = (CD_90 + CD_270)/2 + ((CD_90 - CD_270) / 2) * math.sin(beta_prim * Datos.pi / 180)
        Log10 = math.log(Re) / math.log(10)
        CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
        #Cálculo del coeficiente de la normal y de la tangencial de la Polar
        CN = (CD_func) * ((math.sin(alpha * Datos.pi / 180)) + 0.0023 * (math.sin(2 * alpha * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(alpha * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(alpha * math.pi / 180)) ** 8))))
        CT = (CD_func) * 0.3 * t_c * (abs(math.sin(alpha * Datos.pi / 180) + 0.1 * math.sin(2 * alpha * Datos.pi / 180))) * (1 - 2 * math.cos(alpha * Datos.pi / 180)) - CD_f * math.cos(alpha * Datos.pi / 180)
        #Cálculo de los coeficientes de sustentación y arrastre
        Cl = CN * math.cos(alpha * Datos.pi / 180) + CT * math.sin(alpha * Datos.pi / 180)
        Cd = (CN * math.sin(alpha * Datos.pi / 180) - CT * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))
        if alpha <= 45 and alpha >= alpha_max_tab :
            #Cálculo de los coeficientes de desprendimiento
            CT_ds_mas = ((Cl_max_tab / math.cos(alpha_max_tab * Datos.pi / 180)) - (Cd_max_tab / math.sin(alpha_max_tab * Datos.pi / 180))) / ((math.sin(alpha_max_tab * Datos.pi / 180) / math.cos(alpha_max_tab * Datos.pi / 180)) + (math.cos(alpha_max_tab * Datos.pi / 180) / math.sin(alpha_max_tab * Datos.pi / 180)))
            CN_ds_mas = (Cl_max_tab - (CT_ds_mas * math.sin(alpha_max_tab * Datos.pi / 180))) / (math.cos(alpha_max_tab * math.pi / 180))
            f_mas = ((alpha - 45) / (alpha_max_tab - 45)) ** 2
            beta_prim = 45 - alphazero * math.cos(45 * Datos.pi / 180)
            CD_func = (CD_90 + CD_270)/2 + ((CD_90 - CD_270) / 2) * math.sin(beta_prim * Datos.pi / 180)
            Log10 = math.log(Re) / math.log(10)
            CD_f = (0.455 / (Log10 ** 2.58)) - (1700 / Re)
            #Coeficientes de separación
            CN_sep = (CD_func) * ((math.sin(45 * Datos.pi / 180)) + 0.0023 * (math.sin(2 * 45 * Datos.pi / 180)) / (0.38 + (0.62 * abs((math.sin(45 * Datos.pi / 180)))) + (3.7 * t_c * ((math.cos(45 * math.pi / 180)) ** 8))))
            CT_sep = (CD_func) * 0.3 * t_c * (abs(math.sin(45 * Datos.pi / 180) + 0.1 * math.sin(2 * 45 * Datos.pi / 180))) * (1 - 2 * math.cos(45 * Datos.pi / 180)) - CD_f * math.cos(45 * Datos.pi / 180)
            #Cálculo del coeficiente de la normal y de la tangencial por interpolación según Lorenzo Battisti
            CN_mas = CN_ds_mas * f_mas + CN_sep * (1 - f_mas)
            CT_mas = CT_ds_mas * f_mas + CT_sep * (1 - f_mas)
            #Coeficientes de sustentación y resistencia
            Cl = CN_mas * math.cos(alpha * Datos.pi / 180) + CT_mas * math.sin(alpha * Datos.pi / 180)
            Cd = (CN_mas * math.sin(alpha * Datos.pi / 180) - CT_mas * math.cos(alpha * Datos.pi / 180)) * (1 - 0.4 * (1 - math.exp(-(11.4) / (Datos.AR / (math.sin(alpha * Datos.pi / 180))))))

    return Cl, Cd