##############################################################
# PROYECTO: OPTIMIZACIÓN DE DESPLIEGUE DE ANTENAS EN SANTIAGO
##############################################################


########################
#     LIBRERÍAS
########################

import numpy as np
import pandas as pd
import folium
from folium import plugins
from scipy.spatial import distance_matrix
from scipy.interpolate import Rbf
import random

# -----------------------------
#    FIJAMOS SEMILLA
# -----------------------------
np.random.seed(123)
random.seed(123)


#######################################
#  DEFINIMOS LAS FUNCIONES A UTILIZAR
#######################################

# -----------------------------
# Calidad de servicio
# -----------------------------

def calcular_calidad(puntos, antenas, alpha=5):
    dist_matrix = distance_matrix(puntos[['lat', 'lon']], antenas[['lat', 'lon']])
    dist_min = np.min(dist_matrix, axis=1)
    calidad = np.maximum(0, 1 - alpha * dist_min)
    return calidad

# --------------------------------
# Interpolación de calidad - RBF
# --------------------------------

def interpolar_rbf(puntos, calidad, grid_size=200):
    lat_grid = np.linspace(lat_min, lat_max, grid_size)
    lon_grid = np.linspace(lon_min, lon_max, grid_size)
    lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)

    rbf = Rbf(puntos['lat'], puntos['lon'], calidad, function='multiquadric')
    calidad_interp = rbf(lat_mesh, lon_mesh)
    return lat_mesh, lon_mesh, calidad_interp

# -----------------------------
# Algoritmo Evolutivo Simple
# -----------------------------

def evolucion(centros_df, antenas_idx_iniciales, puntos_evaluacion, max_generaciones=30, p_mut=0.3):
    antenas_fijas = set(antenas_idx_iniciales)
    antenas_actuales = set(antenas_idx_iniciales)
    mejor_calidad = np.mean(calcular_calidad(puntos_evaluacion, centros_df.iloc[list(antenas_actuales)]))

    for generacion in range(max_generaciones):
        nuevo_antenas = antenas_actuales.copy()

        if random.random() < p_mut and len(nuevo_antenas) < 36:
            posibles = set(range(36)) - nuevo_antenas
            nuevo_antenas.add(random.choice(list(posibles)))

        nueva_calidad = np.mean(calcular_calidad(puntos_evaluacion, centros_df.iloc[list(nuevo_antenas)]))

        if nueva_calidad > mejor_calidad:
            antenas_actuales = nuevo_antenas
            mejor_calidad = nueva_calidad
            print(f"Generación {generacion}: Mejor calidad = {mejor_calidad:.4f}, N° antenas = {len(antenas_actuales)}")

    return list(antenas_actuales)


######################################
#   EJECUTAMOS EL PROCESO COMPLETO
######################################


# --------------------------------------
# 1. Dividir Santiago en 36 cuadrantes
# --------------------------------------

lat_min, lat_max = -33.6, -33.3
lon_min, lon_max = -70.8, -70.5

latitudes = np.linspace(lat_min, lat_max, 7)
longitudes = np.linspace(lon_min, lon_max, 7)

centros = []
for i in range(6):
    for j in range(6):
        lat_centro = (latitudes[i] + latitudes[i+1]) / 2
        lon_centro = (longitudes[j] + longitudes[j+1]) / 2
        centros.append((lat_centro, lon_centro))

centros_df = pd.DataFrame(centros, columns=['lat', 'lon'])

# ---------------------------------------------------
# 2. Inicializar 8 antenas en centroides aleatorios
# ---------------------------------------------------

antenas_idx_iniciales = random.sample(range(36), 8)
antenas_iniciales = centros_df.iloc[antenas_idx_iniciales].reset_index(drop=True)

# -------------------------------------------------------------
# 3. Creamos 60 puntos de evaluación de calidad del servicio
# -------------------------------------------------------------

puntos_evaluacion = pd.DataFrame({
    'lat': np.random.uniform(lat_min, lat_max, 60),
    'lon': np.random.uniform(lon_min, lon_max, 60)
})

# ---------------------------------
# 7. Ejecutar el proceso completo
# ---------------------------------

# Calidad inicial
tags_inicial = calcular_calidad(puntos_evaluacion, antenas_iniciales)
puntos_evaluacion['calidad_inicial'] = tags_inicial

# Interpolación inicial
lat_mesh_inicial, lon_mesh_inicial, calidad_interp_inicial = interpolar_rbf(puntos_evaluacion, puntos_evaluacion['calidad_inicial'])

# Optimizar
top_antenas_idx = evolucion(centros_df, antenas_idx_iniciales, puntos_evaluacion)
top_antenas = centros_df.iloc[top_antenas_idx]

# Recalcular calidad final
tags_final = calcular_calidad(puntos_evaluacion, top_antenas)
puntos_evaluacion['calidad_final'] = tags_final
lat_mesh_final, lon_mesh_final, calidad_interp_final = interpolar_rbf(puntos_evaluacion, puntos_evaluacion['calidad_final'])

# Crear mapa Folium combinado
m = folium.Map(location=[-33.45, -70.65], zoom_start=11)

# Dibujar cuadrantes
for lat in latitudes:
    folium.PolyLine(locations=[(lat, lon_min), (lat, lon_max)], color='gray', weight=1).add_to(m)
for lon in longitudes:
    folium.PolyLine(locations=[(lat_min, lon), (lat_max, lon)], color='gray', weight=1).add_to(m)

# Crear capas
inicial_layer = folium.FeatureGroup(name='Calidad Inicial')
final_layer = folium.FeatureGroup(name='Calidad Final')

# Heatmap inicial
heat_data_inicial = [[lat_mesh_inicial[i, j], lon_mesh_inicial[i, j], calidad_interp_inicial[i, j]] for i in range(lat_mesh_inicial.shape[0]) for j in range(lat_mesh_inicial.shape[1])]
plugins.HeatMap(heat_data_inicial, radius=8, blur=15, min_opacity=0.3, max_zoom=11).add_to(inicial_layer)

# Heatmap final
heat_data_final = [[lat_mesh_final[i, j], lon_mesh_final[i, j], calidad_interp_final[i, j]] for i in range(lat_mesh_final.shape[0]) for j in range(lat_mesh_final.shape[1])]
plugins.HeatMap(heat_data_final, radius=8, blur=15, min_opacity=0.3, max_zoom=11).add_to(final_layer)

# Antenas iniciales (también en la capa final)
for idx in antenas_idx_iniciales:
    row = centros_df.iloc[idx]
    folium.Marker(location=[row['lat'], row['lon']], icon=folium.Icon(color='blue', icon='signal'), tooltip=f"Antena Inicial {idx}").add_to(inicial_layer)
    folium.Marker(location=[row['lat'], row['lon']], icon=folium.Icon(color='blue', icon='signal'), tooltip=f"Antena Inicial {idx}").add_to(final_layer)

# Nuevas antenas
for idx in set(top_antenas_idx) - set(antenas_idx_iniciales):
    row = centros_df.iloc[idx]
    folium.Marker(location=[row['lat'], row['lon']], icon=folium.Icon(color='red', icon='plus'), tooltip=f"Antena Nueva {idx}").add_to(final_layer)

# Puntos de evaluación
for idx, row in puntos_evaluacion.iterrows():
    folium.CircleMarker(location=[row['lat'], row['lon']], radius=3, color='black', fill=True, fill_opacity=1).add_to(m)

# Añadir capas al mapa
inicial_layer.add_to(m)
final_layer.add_to(m)

# Añadir control de capas
folium.LayerControl().add_to(m)

# Guardar mapa
m.save("mapa_completo.html")

# -----------------------------
# 8. Resultados
# -----------------------------

print("\nResumen de optimización:")
print(f"Calidad promedio inicial: {np.mean(tags_inicial):.4f}")
print(f"Calidad promedio final: {np.mean(tags_final):.4f}")
print(f"Antenas iniciales: {len(antenas_idx_iniciales)}")
print(f"Antenas finales: {len(top_antenas_idx)}")
print(f"Antenas agregadas: {len(set(top_antenas_idx) - set(antenas_idx_iniciales))}")
