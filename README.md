# Novena versión (06-08)

El módulo de resultados principales es Main_Module. Este módulo ejecuta el cálculo de los archivos de datos y las gráficas principales.

En Helice_Module se calculan la tracción, la potencia y el rendimiento propulsivo. La función principal del módulo es helice(). Los resultados se obtienen en formato .csv a través de la función csv_complete(). Hay funciones de plot para dichos .csv.

En Aircraft_Module se encuentra la función principal() que devuelve resultados de posición, velocidad, aceleración, resistencia, tracción y potencia. Contiene también funciones que generan los .csv y las gráficas necesarias.
 
Camber_Module calcula curvatura, curvatura máxima, curvatura media, espesor y espesor máximo del perfil con el .csv de sus coordenadas. Tiene una función que grafica el perfil y su curvatura.

El módulo Interpolate_Extrapolate_Module calcula los coeficientes de resistencia y sustentación para cualquier ángulo de ataque y número de Reynolds.

Chord_Twist_Module calcula los valores de cuerda y torsión para cada radio de la pala.

Airfoil_Module calcula las coordenadas del perfil para cada radio de la pala y los archivos de Reynolds asociados al perfil que se introducen en Interpolate_Extrapolate_Module.

Los resultados se guardan en la carpeta Archivos_Resultados.

