# Cuarta versión (09-05)
Los módulos de resultados principales son Helice_Module y Main_Module.

En Helice_Module se pueden obtener los resultados de tracción, potencia y rendimiento propulsivo. La función principal del módulo es helice(). Los resultados se obtienen en formato .csv a través de la función csv_complete(). Hay funciones de plot para dichos .csv.
Éstas y otras gráficas relevantes del código se encuentran en la carpeta gráficas.

En Main_Module se encuentra la función principal() que devuelve resultados de posición, velocidad, aceleración, resistencia, tracción y potencia. Contiene también funciones que general los .csv y las gráficas necesarias.

Otros módulos relevantes son Camber_Module e Interpolate_Extrapolate_Module. 
Camber_Module calcula curvatura, curvatura máxima, curvatura media, espesor y espesor máximo del perfil con el .csv de sus coordenadas. Tiene una función que grafica el perfil y su curvatura.

El módulo Interpolate_Extrapolate_Module calcula los coeficientes de resistencia y sustentación para cualquier ángulo de ataque y número de Reynolds.

