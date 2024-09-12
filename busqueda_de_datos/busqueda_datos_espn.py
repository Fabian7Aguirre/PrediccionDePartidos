from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

'''
Fabian Israel Aguirre Mancillas 07/08/24
Parte numero 1.0
'''


# Inicializamos driver para manejo de pagina web
path = 'C:/Users/Fabia/OneDrive/Documentos/chromedriver-win64/chromedriver.exe'
service = Service(executable_path=path)        
opciones = Options()
opciones.add_argument("--disable-popup-blocking") # Desactiva el bloqueo de popups  
driver = webdriver.Chrome(service=service, options=opciones)


def buscar_equipo(equipo):
    '''
        Realiza la busqueda de un equipo en la pagina de ESPN y navega hasta la sección de resultados
    '''
    # Abrimos pagina
    driver.get('https://www.espn.com.mx/')
    #time.sleep(8)
    # Cerrar el iframe de anuncio si es posible
    try:
        close_ad = WebDriverWait(driver, 10).until(driver.find_element(By.ID, 'sprite close'))
        close_ad.click()
    except:
        pass
    # Esperamos a que el elmento sea clickeable y da click
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'global-search-trigger'))).click()
    # Asignamos la caja de busqueda a una variable
    caja_de_busqueda = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'global-search-input')))
    # Escribimos el equipo en la caja de busqueda
    caja_de_busqueda.send_keys(equipo)
    # Damos click en la primer opción
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//li[@class="search_results__item"][1])[1]'))).click()
    # Damos click en la pestaña "Resultados"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//li[@class="Nav__Secondary__Menu__Item flex items-center n7 relative n7 Nav__AccessibleMenuItem_Wrapper"][2]'))).click()
    driver.implicitly_wait(20)

def extraer_resultados(año):
    """
        Extrae los resultados de los partidos desde la tabla visible en la página actual.
    """
    #xPath que usaremos para recabar la información fecha, home, resultado y away de año propuesto, una vez se haya cargado
    matches = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="Table__TR Table__TR--sm Table__even"]')))
    year, fecha, home, resultado, away = [], [], [], [], []

    for match in matches:
        year.append(año)
        fecha.append(match.find_element(By.XPATH, './td[1]').text)
        home.append(match.find_element(By.XPATH, './td[2]').text)
        resultado.append(match.find_element(By.XPATH, './td[3]//span[1]/a[2]').text)
        away.append(match.find_element(By.XPATH, './td[4]').text)

    # Retornamos un dataframe
    return pd.DataFrame({'Año': año,'Fecha': fecha, 'Home': home, 'Resultado': resultado, 'Away': away})

def cambiar_agno_url(año, url):
    """
    Modifica la URL actual para incluir el año o temporada deseada.
    """
    partes = url.split('/')
    partes[-1] = 'temporada'
    partes.append(año)
    return '/'.join(partes)

def driver_quit():
    driver.quit()

def entrar_a_pag_resultados(equipo, bandera, *año):
    """
    Ingresa a la página de resultados del equipo y extrae la información de los partidos.
    """
    try:
        # Si el contador es igual a 0 y año contiene un valor prosigue con la recolección de datos
        if bandera == True:
            año = 2023
            # Llamamos al metodo buscar_equipipo y pasamos equipo a buscar
            buscar_equipo(equipo)
            # Llamamos al metodo extraer_resultados y los resultados dataframe los asignamos a una variable df_resultados
            df_resultados = extraer_resultados(str(año+1))
            url_actual = driver.current_url
            nueva_url = cambiar_agno_url(str(año),url_actual)
            driver.get(nueva_url)
        else:
            año = '2023'
            df_resultados = extraer_resultados(año)
        # Retornamos el data frame
        return df_resultados
    except WebDriverException as e:
        print(f'Error al cargar la pagina o interactuar con el WebDriver: {e}')
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")