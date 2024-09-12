import pandas as pd
from datetime import date
from busqueda_de_datos.obtencion_data_historica_dos_equipos import obtencion_data_historica_dos_equipos
from acomodo_de_datos.limpieza_data_historica_dos_equipos import limpieza_data_historica_dos_equipos
from analisis_de_datos.obtencion_porcentajes_casa import lanzar_puntuación_general_casa
from analisis_de_datos.obtencion_porcentajes_visita import lanzar_puntuación_general_visita

# Fecha
hoy = date.today()

# Equipos a analizar
casa = 'Correcaminos'
visita= 'Oaxaca'

def resultados(casa, visita):


    # Consultamos data historica de ambos equipos y obtenemos un dataframe
    # Esta función genera un archivo csv
    df_equipos = obtencion_data_historica_dos_equipos(casa, visita)

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

    # Guardamos los dataframe de los analisis
    # Crear un objeto ExcelWriter
    nombre_hoja = f'{casa} vs {visita} - {date.today()}'
    if len(nombre_hoja) > 30:
        nombre_hoja = f'{casa[:10]} vs {visita[:10]}'
    with pd.ExcelWriter('Analisis.xlsx') as writer:
        # Guardamos el primer DataFrame Casa
        df_analisis_casa.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=0,)
        # Guardamos el segundo DataFrame Visita
        df_analisis_visita.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=len(df_analisis_casa) + 2)

resultados(casa, visita)