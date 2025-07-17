import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
from scipy.stats import mode
from carga_datos import carga_union_datos
df_union=carga_union_datos();

#Aqui realizaremos la limpieza de los datos que utilizaremos.
#A partir del análisis de valores perdidos decidimos realizar una limpieza de estos datos, vamos a proceder a eliminar la columna unnamed ya que no aporta valor.
#Tambien decidimos realizar el analisis sobre la modalidad fulltime por lo que eliminaremos del dataset los valores pertenecientes a la modalidad part time.

#Limpieza de algunos campos de los datos, y creacion de columnas para las graficas 
#para evitar errores convierto a numero la que se que necesito que lo sea
def limpieza_datos(df_union):
    df_union = df_union.drop('Unnamed', axis=1, errors='ignore')
    df_union = df_union[df_union['Dedicacion'] != 'Part-Time']
    df_union = df_union.reset_index(drop=True)
    df_union['Experiencia'] = pd.to_numeric(df_union['Experiencia'], errors='coerce')
    df_union['Nacimiento']=pd.to_numeric(df_union['Nacimiento'],errors='coerce')
    df_union['Ultimo salario (Neto)'] = pd.to_numeric(df_union['Ultimo salario (Neto)'], errors='coerce') 
    df_union = df_union.dropna(subset=['Ultimo salario (Neto)'])
    herramientas_cols = ['Plataforma (actual)', 'Software utilizado', 'Framework -Librerias', 'Bases de Datos', 'QA-Testing']
    df_union['Cantidad de herramientas usadas'] = df_union[herramientas_cols].notna().sum(axis=1)
    df_union['Edad'] = pd.to_datetime(df_union['Fecha encuesta']).dt.year - df_union['Nacimiento']
    return df_union
    
def crear_df_burbuja(df_union):
     df_burbuja = df_union.dropna(subset=['Experiencia', 'Ultimo salario (bruto)', 'Modalidad', 'Cantidad de herramientas usadas'])
     return df_burbuja



