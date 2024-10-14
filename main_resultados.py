import pandas as pd
import os
import pickle
from datetime import date
from busqueda_de_datos.obtencion_data_historica_dos_equipos import obtencion_data_historica_dos_equipos
from acomodo_de_datos.limpieza_data_historica_dos_equipos import limpieza_data_historica_dos_equipos
from analisis_de_datos.obtencion_porcentajes_casa import lanzar_puntuación_general_casa
from analisis_de_datos.obtencion_porcentajes_visita import lanzar_puntuación_general_visita

# Fecha
hoy = date.today()

agnos = 2024, 2023, 2022

# Equipos a analizar
#casa = 'Mazatlán FC'
#visita= 'Necaxa'


def resultados(casa, visita, *agnos):


    # Consultamos data historica de ambos equipos y obtenemos un dataframe
    # Esta función genera un archivo csv
    df_equipos = obtencion_data_historica_dos_equipos(casa, visita, agnos)

    # Limpiamos dataframe y lo guarda en un nuevo csv
    limpieza_data_historica_dos_equipos()

    # Hacemos analisis de ambos equipos con la información obtenida
    conclucion_casa = lanzar_puntuación_general_casa(casa)
    conclucion_visita = lanzar_puntuación_general_visita(visita)


    '''# Obtenemos toda la ifnormación que nos retornaron lanzar_puntuación_general_casa y lanzar_puntuación_general_visita
    dict_analisis_casa = conclucion_casa
    dict_analisis_visita = conclucion_visita'''

    # Los convertimos en DF
    df_analisis_casa = pd.DataFrame(conclucion_casa)
    df_analisis_visita = pd.DataFrame(conclucion_visita)

    # Mandamos llamar a la funcion posible_ganador() para obtener un nuevo df con esta información
    df_posible_ganador = posible_ganador(df_analisis_casa, df_analisis_visita)

    # Guardamos los dataframe de los analisis
    # Crear un objeto ExcelWriter
    nombre_hoja = f'{casa[:3]} vs {visita[:3]} - {date.today()}'
    nombre_archivo = 'AnalisisPRINCIPAL.xlsx'

    if os.path.exists(nombre_archivo):
        with pd.ExcelWriter(nombre_archivo, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
            # Guardamos el primer DataFrame Casa
            df_analisis_casa.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=0,)
            # Guardamos el segundo DataFrame Visita
            df_analisis_visita.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=len(df_analisis_casa) + 2)
            # Guardamos el tercer DataFrame Posible Ganador
            df_posible_ganador.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=len(df_analisis_visita) + 2 + len(df_analisis_casa) + 2)
    else:
        with pd.ExcelWriter(nombre_archivo) as writer:
            # Guardamos el primer DataFrame Casa
            df_analisis_casa.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=0,)
            # Guardamos el segundo DataFrame Visita
            df_analisis_visita.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=len(df_analisis_casa) + 2)
            # Guardamos el tercer DataFrame Posible Ganador
            df_posible_ganador.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=len(df_analisis_visita) + 2 + len(df_analisis_casa) + 2)

def posible_ganador(df_analisis_casa, df_analisis_visita):
    '''
        Comparamos la diferencias de puntuación general para obtener el posible ganador
    '''
    if df_analisis_casa['Puntuacion General %'][0] > df_analisis_visita['Puntuacion General %'][0]:
        ganador = df_analisis_casa['Equipo'][0]
        porcentaje = df_analisis_casa['Puntuacion General %'][0] - df_analisis_visita['Puntuacion General %'][0]
    elif df_analisis_visita['Puntuacion General %'][0] > df_analisis_casa['Puntuacion General %'][0]:
        ganador = df_analisis_visita['Equipo'][0]
        porcentaje = df_analisis_visita['Puntuacion General %'][0] - df_analisis_casa['Puntuacion General %'][0]
    else:
        ganador = 'Empate'
        porcentaje = 0

    df_diferencia = {
        'Equipo': [ganador],
        'A favor %': [porcentaje]
    }

    df_diferencia = pd.DataFrame(df_diferencia)

    return df_diferencia

def abrir_dict():
    #Abrimos diccionarios y los asignamos a un dataframe
    with open('dict_versus_UEFA', 'rb') as file:
        df_versus = pickle.load(file)
    return df_versus

df_versus = abrir_dict()
df_data_equipos = []

'''for index, row in df_versus.iterrows():
    resultados(row['Casa'], row['Visita'])
'''    

resultados('Pumas UNAM', 'Atlético de San Luis')