from busqueda_datos_espn import inicializar_driver, driver_quit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime
import re

# Inicializamos driver y lo asignamos a variable


def buscar_posiciones(driver):
    '''
        Abre pagina de posiciones
    '''
    # Abrimos pagina
    driver.get('https://www.espn.com.mx/futbol/posiciones/_/liga/mex.1/temporada/2024')

def extraer_posiciones(driver):
    """
        Extraemos la tabla posiciones
    """
    xpath = '(//tr[@class="Table__TR Table__TR--sm Table__even"] | // tr[@class="filled Table__TR Table__TR--sm Table__even"])//span[4]'
    xpath_2= '(//tbody[@class="Table__TBODY"])[2]//tr'
    #xPath que usaremos para recabar la información fecha, home, resultado y away de año propuesto, una vez se haya cargado
    matches = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    matches_2 = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath_2)))
    equipo, partidos, partidos_ganados, empates, derrotas, goles_a_favor, goles_en_contra, diferencia, puntos = [], [], [], [], [], [], [], [], []
    for match in matches:
        equipo.append(match.text)
    for match in matches_2:
        partidos.append(match.find_element(By.XPATH, './td[1]').text)
        partidos_ganados.append(match.find_element(By.XPATH, './td[2]').text)
        empates.append(match.find_element(By.XPATH, './td[3]').text)
        derrotas.append(match.find_element(By.XPATH, './td[4]').text)
        goles_a_favor.append(match.find_element(By.XPATH, './td[5]').text)
        goles_en_contra.append(match.find_element(By.XPATH, './td[6]').text)
        diferencia.append(match.find_element(By.XPATH, './td[7]').text)
        puntos.append(match.find_element(By.XPATH, './td[8]').text)
    
    df_resultados = pd.DataFrame({'Equipo': equipo,'# P': partidos, 'P G': partidos_ganados, 'E':empates,'P P': derrotas, 'G F': goles_a_favor, 'G C': goles_en_contra, 'D':diferencia, 'Puntos': puntos})

    return df_resultados

def extraer_ids_365_scores(driver):
    # Abre pagina de 365 scores
    driver.get('https://www.365scores.com/es-mx/football/league/liga-mx-141/standings')
    # xpath que usaremos para extraer tabla
    xpath = '//table[@class="table"]//tr'
    matches = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    posicion, id, equipo, partidos, partidos_ganados, empates, derrotas, goles_a_favor, goles_en_contra, diferencia, puntos = [], [], [], [], [], [], [], [], [], [], []

    for match in matches[1:]:
        posicion.append(match.find_element(By.XPATH, './td[2]').text)
        # Obtenemos el id que maneja la pagina de la siguiente manera
        # Mediante el atributo 'href' que contiene ./td[2]/a le aplicamos la expresión regular para separar los ultimos digitos del enlace
        href = re.search(r'(\d+)$',match.find_element(By.XPATH, './td[2]/a').get_attribute("href")).group(1)
        id.append(href)
        equipo.append(match.find_element(By.XPATH, './td[3]').text)
        partidos.append(match.find_element(By.XPATH, './td[4]').text)
        partidos_ganados.append(match.find_element(By.XPATH, './td[8]').text)
        empates.append(match.find_element(By.XPATH, './td[9]').text)
        derrotas.append(match.find_element(By.XPATH, './td[10]').text)
        goles = match.find_element(By.XPATH, './td[5]').text
        goles = goles.split(':')
        goles_a_favor.append(goles[0])
        goles_en_contra.append(goles[1])
        diferencia.append(match.find_element(By.XPATH, './td[6]').text)
        puntos.append(match.find_element(By.XPATH, './td[7]').text)

    df_resultados = df_resultados = pd.DataFrame({'':posicion, 'ID':id, 'Equipo': equipo,'# P': partidos, 'P G': partidos_ganados, 'E':empates,'P P': derrotas, 'G F': goles_a_favor, 'G C': goles_en_contra, 'D':diferencia, 'Puntos': puntos})

    return df_resultados
driver = inicializar_driver()

#buscar_posiciones(driver)
#print(extraer_posiciones(driver))
print(extraer_ids_365_scores(driver))
#driver_quit()