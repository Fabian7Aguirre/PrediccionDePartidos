import requests
import pandas as pd
import pickle
import time
from datetime import datetime

#https://site.web.api.espn.com/apis/v2/sports/soccer/mex.1/standings?region=mx&lang=es&contentorigin=deportes&seasontype=1&season=2022&sort=rank%3Aasc
#https://site.web.api.espn.com/apis/site/v2/sports/soccer/MEX.1/teams/220/schedule?region=mx&lang=es&season=2024
def obtener_json(url):
    '''
        1- Abrimos devtools en chrome
        2.- Vamos a la pestaña de network
        3.- Filtramos peticiones XHR/Fetch/Other
        4.- Analizamos las peticiones que contengan datos relevantes
        5.- Clic en la petición y seleccionamos response
        6.- En pestaña Headers buscamos la Request URL
        7.- Copiamos la URL y la usamos para ver si tiene datos JSON
    '''
    # URL de la API o AJAX que carga los datos
    api_url = url

    # Realiza una petición GET a la API
    response = requests.get(api_url)

    # Verifica si la petición fue exitosa
    if response.status_code == 200:
        data = response.json()  # O response.text si es HTML
        #print(data)  # Aquí puedes procesar y almacenar los datos como prefieras
    else:
        print("Error al obtener los datos:", response.status_code)
    return data

def df_tabla_posiciones(data):
    '''
        Extraemos los ids, los nombres y datos de los equipos del json "data"
    '''
    id_equipos, equipos, partidos_jugados, partidos_ganados, empates, derrotas, goles_favor, goles_contra, diferencia, pts = [], [], [], [], [], [], [], [], [], []
    data = data['children'][0]['standings']['entries']

    # Recorremos "competitions"
    for team in data:
        id_equipos.append(team['team']['id'])
        equipos.append(team['team']['name'])
        partidos_jugados.append(team['stats'][0]['value'])
        partidos_ganados.append(team['stats'][7]['value'])
        empates.append(team['stats'][6]['value'])
        derrotas.append(team['stats'][1]['value'])
        goles_favor.append(team['stats'][5]['value'])
        goles_contra.append(team['stats'][4]['value'])
        diferencia.append(team['stats'][2]['value'])
        pts.append(team['stats'][3]['value'])

    df_tabla_equipos = pd.DataFrame({'ID':id_equipos, 'Equipo':equipos, 'Partidos jugados': partidos_jugados, 
                                     'Partidos ganados': partidos_ganados, 'Empates': empates,
                                     'Derrotas': derrotas, 'Goles a favor': goles_favor,
                                     'Goles en contra': goles_contra, 'Diferencia': diferencia,
                                     'PTS': pts})

    return df_tabla_equipos

def convertir_fecha(fecha):
    # Convertir la cadena a un objeto datetime
    fecha = datetime.strptime(fecha, '%Y-%m-%dT%H:%MZ')

    # Convertir el formato datetime a el formato deseado
    fecha = fecha.strftime('%Y-%m-%d')

    return fecha

def partidos(data):
    home_competitor, score_home, away_competitor, score_away, fecha, home_record, away_record = [], [], [], [], [], [], []
    events = data['events']
    for event in events:
        fecha_event = convertir_fecha(event['date'])
        fecha.append(fecha_event)
        home_competitor.append(event['competitions'][0]['competitors'][0]['team']['displayName'])
        score_home.append(event['competitions'][0]['competitors'][0]['score']['value'])
        away_competitor.append(event['competitions'][0]['competitors'][1]['team']['displayName'])
        score_away.append(event['competitions'][0]['competitors'][1]['score']['value'])
        home_record.append(event['competitions'][0]['competitors'][0]['record'][0]['displayValue'])
        away_record.append(event['competitions'][0]['competitors'][1]['record'][0]['displayValue'])

    return pd.DataFrame({'Fecha':fecha, 'H-Record': home_record, 'Home': home_competitor, 
                         'H-Score': score_home, 'A-Score': score_away, 'Away': away_competitor, 
                         'A-Record': away_record})

def guardar_df(nombre_df, df_tabla):
    try:
            with open(nombre_df, 'wb') as output:
                pickle.dump(df_tabla, output)
            df_tabla.to_csv(nombre_df+'.csv', index=False)
    except FileExistsError:
        print('El archivo no existe.')
    except IOError:
        print("Error de entrada/salida.")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

def df_todos_partidos_LMX():
    # Obtenemos el id de cada equipo
     # Abrimos archivo  y los asignamos a un dataframe
    # Agregamos el parametro encoding='utf-8 para que pueda leer todos los caracteres del archivo
    with open('df_2023_LMX.csv', 'r', encoding='utf-8') as file:
        df_equipos = pd.read_csv(file)
    list_partidos = []
    for i, row in df_equipos.iterrows():
        data = obtener_json(f'https://site.web.api.espn.com/apis/site/v2/sports/soccer/MEX.1/teams/{row['ID']}/schedule?region=mx&lang=es&season=2024')
        df_partidos_de_equipo = partidos(data)
        print(type(df_partidos_de_equipo))
        time.sleep(1.5)
        list_partidos.append(df_partidos_de_equipo)
    
    df_todos_los_partidos = pd.concat(list_partidos, ignore_index=True)



    guardar_df('Historial_2024_LGM.csv', df_todos_los_partidos)



df_todos_partidos_LMX()