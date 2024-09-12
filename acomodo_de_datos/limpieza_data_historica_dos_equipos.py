import pandas as pd

'''
Fabian Israel Aguirre Mancillas 07/08/24
Parte numero 3.0
'''
def convertir_fecha(fecha):
    '''
        Hacemos un split donde separamos la cadena fecha por sus espacios en blanco
        Ignoramos el dia de la semana, asignamos el dia numerico a "dia", posterior a eso utilizamos strip para eliminar "."
        y asi asignamos el mes. Juntamos estos dos en la variable "fecha"
    '''
    partes = fecha.split()
    dia = partes[1]
    mes = partes[3].strip('.')
    fecha = (f'{dia}-{mes}-')
    return fecha

def remplazar_fecha(df_equipos):
    fechas = df_equipos['Fecha']
    '''
        Creamos un dataframe de todas las fechas de partidos donde tengan el nuevo formato
        Asignamos este dataframe al original y posteriormente combinamos esta columna "Fecha" con la columna "Año"
    '''
    fechas_split = fechas.apply(lambda x: pd.Series(convertir_fecha(x)))
    fechas_split.rename(columns={0:'Fecha'}, inplace=True)
    df_equipos['Fecha'] = fechas_split
    df_equipos['Fecha'] = df_equipos.apply(lambda row: f'{row['Fecha']}{row['Año']}', axis=1)
    return df_equipos

def elimina_espacios_blancos(df_equipos):
    # Eliminamos espacios en blanco al principio y al final de las cadenas
    df_equipos['Home'] = df_equipos['Home'].str.strip()
    df_equipos['Away'] = df_equipos['Away'].str.strip()
    df_equipos['Resultado'] = df_equipos['Resultado'].str.strip()
    # Eliminamos valos NA 
    df_equipos.dropna(inplace=True)
    return df_equipos

def eliminar_duplicados(df_equipos):
    # Eliminamos duplicados
    df_equipos.drop_duplicates(inplace=True)
    # Ordenamos por equipos y luego fechas
    df_equipos.sort_values(by=['Home', 'Fecha'], ascending=[True, False], inplace=True)
    return df_equipos

def acomodo_df(df_equipos):
    # Dividimos el marcador para agregar una columna para goles anotados y otra para goles recibidos
    df_equipos[['Goles Home', 'Goles Away']] = df_equipos['Resultado'].str.split('-', expand=True)
    df_equipos.drop('Resultado', axis=1, inplace=True)
    df_equipos.drop('Año', axis=1, inplace=True)
    df_equipos.sort_values(by=['Home', 'Fecha'], ascending=[True, True], inplace=True)
    return df_equipos

def limpieza_data_historica_dos_equipos():
    # Abrimos archivo  y los asignamos a un dataframe
    # Agregamos el parametro encoding='utf-8 para que pueda leer todos los caracteres del archivo
    with open('data_historica_versus.csv', 'r', encoding='utf-8') as file:
        df_equipos = pd.read_csv(file)


    '''
        Limpiearemos columna por columa
        Extraeremos el día y el mes
    '''

    df_equipos = remplazar_fecha(df_equipos)
    df_equipos = elimina_espacios_blancos(df_equipos)
    df_equipos = eliminar_duplicados(df_equipos)
    df_equipos =acomodo_df(df_equipos)
    # Guardamos el el dataframe actualizado
    df_equipos.to_csv('clean_data_historica_versus.csv', encoding='utf-8', index=False)
    return df_equipos