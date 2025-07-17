import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
from scipy.stats import mode
from carga_datos import carga_union_datos
from Limpieza_datos import limpieza_datos, crear_df_burbuja
#LA HIPOTESIS Y LA INTERPRETACION DE LAS GRAFICAS SE ENCUENTRAN EN EL ARCHIVO README.md 
#DEL REPOSITORIO DE GITHUB CARGADO.

df_union = carga_union_datos()
df_limpio = limpieza_datos(df_union)
df_burbuja = crear_df_burbuja(df_limpio)

#PREGUNTAS CLAVE
#1. Como varía el salario promedio según el nivel de estudios, el género y la experiencia laboral?
df_limpio['Experiencia'] = pd.cut(
    df_limpio['Experiencia'],
    bins=[0,1,5,10,20,50],
    labels=['0 años', '1-5 años', '6-10 años', '11-20 años', '20+ años']
)
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_limpio, x='Nivel de estudio', y='Ultimo salario (bruto)', hue='Genero')
plt.title('Salario según nivel de estudios y genero')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
plt.tight_layout()
plt.show()

#2. Influye la modalidad de trabajo, la experiencia y el tipo de herramientas tecnológicas utilizadas en el salario?
# procedo a contar la cantidad de herramientas
herramientas_cols = ['Plataforma (actual)', 'Software utilizado', 'Framework -Librerias', 'Bases de Datos', 'QA-Testing']
#hacemos la grafica
plt.figure(figsize=(12, 6))
for modalidad in df_burbuja['Modalidad'].unique():
    subset = df_burbuja[df_burbuja['Modalidad'] == modalidad]
    plt.scatter(
        subset['Experiencia'],
        subset['Ultimo salario (bruto)'],
        s=subset['Cantidad de herramientas usadas'] * 40,
        alpha=0.5,
        label=modalidad
)
plt.xlabel('Experiencia')
plt.ylabel('Ultimo salario (bruto)')
plt.title('Sueldo segun modalidad trabajada y experiencia')
plt.legend(title='Modalidad de trabajo')
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
plt.tight_layout()
plt.show()

#3 Qué modalidad de trabajo presenta el salario neto promedio más alto y cómo es este valor con respecto a la moda de los salarios netos?
#Para este grafico me parecio interesante agregar la moda de los sueldos netos, para ello
salario_neto = pd.to_numeric(df_limpio['Ultimo salario (Neto)'], errors='coerce').dropna()
moda_salario_neto=mode(salario_neto,keepdims=True).mode[0]
df_agrup=df_limpio.groupby('Modalidad')['Ultimo salario (Neto)'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
sns.barplot(x=df_agrup.index, y=df_agrup.values, palette='viridis')
plt.axhline(moda_salario_neto, color='red', linestyle='--', label=f'Moda salario neto: {moda_salario_neto:,.0f}')
plt.title('Salario neto promedio por modalidad de trabajo')
plt.xlabel('Modalidad de trabajo')
plt.ylabel('Salario neto promedio')
plt.legend()
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
plt.tight_layout()
plt.show()

#4 Que cantidad de los encuestados recibieron una, dos, tres o mas actualizacion en el periodo 2022?
plt.figure(figsize=(12,6))
actualizaciones=df_limpio['Actualizaciones en 2022'].value_counts().sort_values(ascending=False)
sns.barplot(
    x=actualizaciones.values,
    y=actualizaciones.index,
    color='skyblue'
)
plt.xlabel('Encuestados')
plt.ylabel('Cantidad de actualizaciones')
plt.title('Actualizaciones en 2022')
plt.gca().xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
plt.tight_layout()
plt.show()

#Analisis de valores perdidos
porcentaje_perdidos=(df_limpio.isnull().mean()*100).round(2)
#como queremos ver los valores perdidos solo nos vamos a quedar con ellos entonces,
porcentaje_perdidos=porcentaje_perdidos[porcentaje_perdidos>0]
porcentaje_perdidos=porcentaje_perdidos.sort_values(ascending=False)

plt.figure(figsize=(12, 6))
bars=plt.bar(porcentaje_perdidos.index, porcentaje_perdidos.values, color='red')
plt.ylabel('Porcentaje de valores perdidos (%)')
plt.title('Porcentaje de valores perdidos por columna')
plt.xticks(rotation=45, ha='right')
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
plt.ylim(0,100)
#para agregar entendimiento le voy a poner etiquetas a cada barra
for bar in bars:
    height=bar.get_height()
    plt.text(
        bar.get_x()+bar.get_width()/2, height+1,f'{height:.2f}%',
        ha='center', va='bottom', fontsize=8, color='black'
    )
plt.tight_layout()
plt.show()

