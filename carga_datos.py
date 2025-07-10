import pandas as pd

def carga_union_datos():
    personales = pd.read_csv(
        'https://github.com/cior666/Trabajo_CoderHouse/raw/refs/heads/main/Datos_personales.csv',
        encoding='latin1',
        sep=';'
    )

    laborales = pd.read_csv(
        'https://github.com/cior666/Trabajo_CoderHouse/raw/refs/heads/main/Datos_laborales.csv',
        encoding='latin1',
        sep=';'
    )
    estudios= pd.read_csv(
        'https://github.com/cior666/Trabajo_CoderHouse/raw/refs/heads/main/Datos_estudios_superiores.csv',
        encoding='latin1',
        sep=';'
    )
    guardias=pd.read_csv(
        'https://github.com/cior666/Trabajo_CoderHouse/raw/refs/heads/main/Datos_Guardias_laborales.csv',
        encoding='latin1',
        sep=';'
    )
    herramientas=pd.read_csv(
        'https://github.com/cior666/Trabajo_CoderHouse/raw/refs/heads/main/Datos_Herramientas.csv',
        encoding='latin1',
        sep=';'
    )

    bootcamps=pd.read_csv(
        'https://github.com/cior666/Trabajo_CoderHouse/raw/refs/heads/main/Datos_Bootcamps.csv',
        encoding='latin1',
        sep=';'
    )
#Agrupo los datos de las tablas
    df_union = personales.merge(laborales, on='ID_Encuestado', how='outer') \
                      .merge(estudios, on='ID_Encuestado', how='outer') \
                      .merge(guardias, on='ID_Encuestado', how='outer') \
                      .merge(herramientas, on='ID_Encuestado', how='outer') \
                      .merge(bootcamps, on='ID_Encuestado', how='outer')
    return df_union