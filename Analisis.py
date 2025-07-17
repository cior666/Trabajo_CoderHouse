import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from carga_datos import carga_union_datos
from Limpieza_datos import limpieza_datos
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import r2_score

df_union = carga_union_datos()
df_limpio = limpieza_datos(df_union)
#Procedemos a hacer el siguiente agrupamiento para hacer un análisis más adelante.
condiciones = [
    df_limpio['Nivel de estudio'].isin([
        'Universitario', 'Posgrado/Especialización', 'Maestría', 'Doctorado', 'Posdoctorado'
    ]),
    df_limpio['Nivel de estudio'].isin([
        'Terciario', 'Secundario', 0
    ])
]
valores = ['Universitario', 'No universitario']
df_limpio['Nivel_agrupado'] = np.select(condiciones, valores, default='No universitario')

##################################################################################################################################
#Vamos a proceder a realizar diversos análisis de regresión y correlación.

#El primero será un análisis entre los años de experiencia laboral y el salario neto.
#En el PDF se explicará por que se realizó el recorte en el rango elegido.
df_experiencia=df_limpio[(df_limpio['Experiencia']>=0) & (df_limpio['Experiencia']<=15)]
exp_salario=df_experiencia.groupby('Experiencia')['Ultimo salario (Neto)'].mean().reset_index()
#Analisis de correlacion
correl=exp_salario['Experiencia'].corr(exp_salario['Ultimo salario (Neto)'])
print(f"Coeficiente de determinación (R²): {correl:.2f}")
X=exp_salario[['Experiencia']]
y=exp_salario['Ultimo salario (Neto)']
modelo=LinearRegression()
modelo.fit(X,y)
y_pred=modelo.predict(X)

pendiente = modelo.coef_[0]
intercepto = modelo.intercept_
print(f"Ecuación de la recta de ajuste: y = {pendiente:.2f} * x + {intercepto:.2f}")
#Procedemos a evaluar la capacidad de extrapolación (explicada en el PDF)
salarios_18 = df_limpio[df_limpio['Experiencia'] == 18]['Ultimo salario (Neto)']
#Calculamos el promedio
promedio_18 = salarios_18.mean()
print(f"El salario neto promedio real para 18 años de experiencia es: {promedio_18:.2f}")
salarios_19 = df_limpio[df_limpio['Experiencia'] == 19]['Ultimo salario (Neto)']
#Calculamos el promedio
promedio_19 = salarios_19.mean()
print(f"El salario neto promedio real para 19 años de experiencia es: {promedio_19:.2f}")
plt.figure(figsize=(10,6))
plt.scatter(exp_salario['Experiencia'], exp_salario['Ultimo salario (Neto)'], label='Promedio por experiencia')
plt.plot(exp_salario['Experiencia'], y_pred, color='red', label='Regresión lineal')
plt.xlabel('Experiencia')
plt.ylabel('Salario Neto Promedio')
plt.title('Relación entre Experiencia y Salario Neto (0-15 años)')
plt.legend()
plt.tight_layout()
plt.show()


#El segundo constará entre edad y salario neto. Tomaremos el rango entre 20 a 45 años que representa adecuadamente la etapa más activa del desarrollo profesional y que evita distorsiones.
# Para hacer los diversos analisis transformare el dataset limpio dependiendo que rangos de variables quiero usar.
df_edad = df_limpio[(df_limpio['Edad'] >= 20) & (df_limpio['Edad'] <= 45)]

# Procedo a hallar el promedio por edad
edad_salario = df_edad.groupby('Edad')['Ultimo salario (Neto)'].mean().reset_index()
# Análisis de correlación
correlacion = edad_salario['Edad'].corr(edad_salario['Ultimo salario (Neto)'])
print(f"Coeficiente de determinación (R²): {correlacion:.2f}")
X = edad_salario[['Edad']]
y = edad_salario['Ultimo salario (Neto)']
modelo = LinearRegression()
modelo.fit(X, y)
y_pred = modelo.predict(X)

pendiente = modelo.coef_[0]
intercepto = modelo.intercept_
print(f"Ecuación de la recta de ajuste: y = {pendiente:.2f} * x + {intercepto:.2f}")

#Buscamos el valor real para hacer la comparación en el PDF.
salarios_20 = df_limpio[df_limpio['Edad'] == 20]['Ultimo salario (Neto)']
#Calculamos el promedio
promedio_20 = salarios_20.mean()
print(f"El salario neto promedio real para 20 años de experiencia es: {promedio_20:.2f}")

plt.figure(figsize=(10,6))
plt.scatter(edad_salario['Edad'], edad_salario['Ultimo salario (Neto)'], label='Promedio por edad')
plt.plot(edad_salario['Edad'], y_pred, color='red', label='Regresión lineal')
plt.xlabel('Edad')
plt.ylabel('Salario Neto Promedio')
plt.title('Relación entre Edad y Salario Neto (20-45 años)')
plt.legend()
plt.tight_layout()
plt.show()


#Analisis integrador de los anteriores
#Analisis de regresion y correlacion de Edad y experiencia laboral.
df_integrador=df_limpio[(df_limpio['Edad']>=18) & (df_limpio['Edad']<=75)]
#Agrupo por la edad del encuestado y el promedio de experiencia
edad_exp = df_integrador.groupby('Edad')['Experiencia'].mean().reset_index()

X = edad_exp['Edad'].values
y = edad_exp['Experiencia'].values

#Realizamos un ajuste polinomico de grado 2 porque es el que nos proporcionaba mejor coeficiente de correlacion
coef = np.polyfit(X, y, 2)
poly_eq = np.poly1d(coef)
y_pred = poly_eq(X)

r2 = r2_score(y, y_pred)
print(f"Ecuación de ajuste: y = {coef[0]:.4f}x² + {coef[1]:.4f}x + {coef[2]:.4f}")
print(f"Coeficiente de determinación (R²) = {r2:.4f}")

#Graficamos
plt.figure(figsize=(10,6))
plt.scatter(X, y, label='Promedio por edad')
plt.plot(X, y_pred, 'k--', label='Ajuste polinómico grado 2')
plt.title('Edad vs Promedio de Experiencia Laboral')
plt.xlabel('Edad')
plt.ylabel('Promedio de Experiencia Laboral')
plt.legend()
plt.tight_layout()
plt.show()

#Por ultimo vamos a realizar dos análisis de regresión más entre personas con o sin formación universitaria
#Para los que no tienen formación universitaria:
df_no_uni = df_limpio[(df_limpio['Nivel_agrupado'] == 'No universitario') & (df_limpio['Edad'] >= 18) & (df_limpio['Edad'] <= 75)]

edad_exp_no_uni = df_no_uni.groupby('Edad')['Experiencia'].mean().reset_index()

X_no_uni = edad_exp_no_uni['Edad'].values
y_no_uni = edad_exp_no_uni['Experiencia'].values
coef_no_uni = np.polyfit(X_no_uni, y_no_uni, 2)
poly_eq_no_uni = np.poly1d(coef_no_uni)
y_pred_no_uni = poly_eq_no_uni(X_no_uni)
r2_no_uni = r2_score(y_no_uni, y_pred_no_uni)

print(f"No universitarios - Ecuación de ajuste: y = {coef_no_uni[0]:.4f}x² + {coef_no_uni[1]:.4f}x + {coef_no_uni[2]:.4f}")
print(f"No universitarios - Coeficiente de determinación (R²) = {r2_no_uni:.4f}")

plt.figure(figsize=(10,6))
plt.scatter(X_no_uni, y_no_uni)
plt.plot(X_no_uni, y_pred_no_uni, 'b--', label='Ajuste polinómico grado 2')
plt.title('No universitarios: Edad - Promedio de Experiencia Laboral')
plt.xlabel('Edad')
plt.ylabel('Promedio de Experiencia Laboral')
plt.tight_layout()
plt.show()

#Para los que tienen formación universitaria.
df_uni = df_limpio[(df_limpio['Nivel_agrupado'] == 'Universitario') & (df_limpio['Edad'] >= 18) & (df_limpio['Edad'] <= 75)]
edad_exp_uni=df_uni.groupby('Edad')['Experiencia'].mean().reset_index()
x_uni=edad_exp['Edad'].values
y_uni=edad_exp['Experiencia'].values
coef_uni=np.polyfit(x_uni, y_uni, 2)
poly_eq_uni = np.poly1d(coef_uni)
y_pred_uni = poly_eq_uni(x_uni)
r2_uni = r2_score(y_uni, y_pred_uni)

print(f"Universitarios - Ecuación de ajuste: y = {coef_uni[0]:.4f}x² + {coef_uni[1]:.4f}x + {coef_uni[2]:.4f}")
print(f"Universitarios - Coeficiente de determinación (R²) = {r2_uni:.4f}")

plt.figure(figsize=(10,6))
plt.scatter(x_uni, y_uni)
plt.plot(x_uni, y_pred_uni, 'b--', label='Ajuste polinómico grado 2')
plt.title('Universitarios: Edad - Promedio de Experiencia Laboral')
plt.xlabel('Edad')
plt.ylabel('Promedio de Experiencia Laboral')
plt.tight_layout()
plt.show()
