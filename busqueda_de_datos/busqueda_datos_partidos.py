import requests
import pandas as pd
import pickle

def obtener_partidos():
    # Obtenemos el id de cada equipo
    # Abrimos archivo  y los asignamos a un dataframe
    # Agregamos el parametro encoding='utf-8 para que pueda leer todos los caracteres del archivo
    with open('df_2023_LMX.csv', 'r', encoding='utf-8') as file:
        df_equipos = pd.read_csv(file)
    df_id_equipos = df_equipos.iloc[:,[0]]
    

    return df_id_equipos

def obtener_json_lmx(id_equipo, año):
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
    api_url = f'https://site.web.api.espn.com/apis/site/v2/sports/soccer/MEX.1/teams/{id_equipo}/schedule?region=mx&lang=es&season={año}'

    # Realiza una petición GET a la API
    response = requests.get(api_url)

    # Verifica si la petición fue exitosa
    if response.status_code == 200:
        data = response.json()  # O response.text si es HTML
        #print(data)  # Aquí puedes procesar y almacenar los datos como prefieras
    else:
        print("Error al obtener los datos:", response.status_code)
    return data

print(obtener_partidos())