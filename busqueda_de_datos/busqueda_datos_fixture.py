# Importamos librerias necesarias para la recolección de datos
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import pickle
import os
import time

'''
Fabian Israel Aguirre Mancillas 07/08/24
Parte numero 1.1
'''
# Inicializamos driver para manejo de pagina web
path = 'C:/Users/Fabia/OneDrive/Documentos/chromedriver-win64/chromedriver.exe'
service = Service(executable_path=path)        
opciones = Options()
opciones.add_argument("--disable-popup-blocking") # Desactiva el bloqueo de popups  
driver = webdriver.Chrome(service=service, options=opciones)

def obtener_datos_LMX():
    '''
        Realiza la busqueda de un equipo en la pagina de ESPN y navega hasta la sección de resultados
    '''
    # Abrimos pagina
    driver.get('https://www.espn.com.mx/futbol/calendario/_/fecha/20241017/liga/mex.1')
    #xPath que usaremos para recabar la información fecha, home, resultado y away de año propuesto, una vez se haya cargado
    matches = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="Table__TR Table__TR--sm Table__even"]')))
    equipo_casa, equipo_visita = [], []

    for match in matches:
        equipo_casa.append(match.find_element(By.XPATH, './td[1]').text)
        equipo_visita.append(match.find_element(By.XPATH, './td[2]//a[2]').text)

    # Retornamos un dataframe
    return pd.DataFrame({'Casa': equipo_casa,'Visita': equipo_visita})

def guardar_dict():
    with open('dict_versus_Liga_MX', 'wb') as output:
        pickle.dump(obtener_datos_LMX(), output)

def guardar_mas_dicts():
    try:
        if os.path.exists('dict_versus_Liga_MX'):
            with open('dict_versus_Liga_MX', 'rb') as output:
                dict_versus_Liga_MX = pickle.load(output)
            nuevo_dict = pd.concat([dict_versus_Liga_MX, obtener_datos_LMX()],ignore_index=True)

            print(nuevo_dict)

            '''with open('dict_versus_Liga_MX', 'wb') as output:
                pickle.dump(nuevo_dict, output)'''
        else:
            with open('dict_versus_Liga_MX', 'wb') as output:
                pickle.dump(obtener_datos_LMX(), output)


    except FileExistsError:
        print('El archivo no existe.')
    except IOError:
        print("Error de entrada/salida.")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

def driver_quit():
    driver.quit()


guardar_mas_dicts()
driver_quit()