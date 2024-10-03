from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime

'''
Fabian Israel Aguirre Mancillas 07/08/24
Parte numero 1.0
'''

def inicializar_driver():
    # Inicializamos driver para manejo de pagina web
    path = 'C:/Users/Fabia/OneDrive/Documentos/chromedriver-win64/chromedriver.exe'
    service = Service(executable_path=path)        
    opciones = Options()
    opciones.add_argument("--disable-popup-blocking") # Desactiva el bloqueo de popups  
    driver = webdriver.Chrome(service=service, options=opciones)
    
    return driver

def buscar_equipo(driver, equipo):
    '''
        Realiza la busqueda de un equipo en la pagina de ESPN y navega hasta la sección de resultados
    '''
    # Abrimos pagina
    driver.get('https://www.espn.com.mx/')
    #time.sleep(8)
    # Cerrar el iframe de anuncio si es posible
    '''try:
        close_ad = WebDriverWait(driver, 10).until(driver.find_element(By.ID, 'sprite close'))
        close_ad.click()
    except:
        pass'''
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
    driver.implicitly_wait(10)

def extraer_resultados(driver, agno):
    """
        Extrae los resultados de los partidos desde la tabla visible en la página actual.
    """
    #xPath que usaremos para recabar la información fecha, home, resultado y away de año propuesto, una vez se haya cargado
    matches = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="Table__TR Table__TR--sm Table__even"]')))
    year, fecha, home, resultado, away = [], [], [], [], []

    for match in matches:
        year.append(agno)
        fecha.append(match.find_element(By.XPATH, './td[1]').text)
        home.append(match.find_element(By.XPATH, './td[2]').text)
        resultado.append(match.find_element(By.XPATH, './td[3]//span[1]/a[2]').text)
        away.append(match.find_element(By.XPATH, './td[4]').text)

    # Retornamos un dataframe
    return pd.DataFrame({'Año': agno,'Fecha': fecha, 'Home': home, 'Resultado': resultado, 'Away': away})

def cambiar_agno_url(agno, url):
    """
        Modifica la URL actual para incluir el año o temporada deseada.
    """
    partes = url.split('/')
    partes[-1] = 'temporada'
    partes.append(agno)
    return '/'.join(partes)

def cambiar_ultimo_segmento(agno, url):
    # Encuentra la posición del último slash
    posicion_ultimo_slash = url.rfind('/')
    
    # Si no hay slash, devuelve la URL original
    if posicion_ultimo_slash == -1:
        return url
    
    # Construye la nueva URL con el nuevo segmento
    nueva_url = url[:posicion_ultimo_slash + 1] + agno
    return nueva_url
    
def driver_quit(driver):

    driver.quit()

def entrar_a_pag_resultados(driver, equipoo, bandera, *agno):
        """
        Ingresa a la página de resultados del equipo y extrae la información de los partidos.
        """
        try:
            # Si el contador es igual a 0 y año contiene un valor prosigue con la recolección de datos
            if bandera == True:
                agno = 2023
                # Llamamos al metodo buscar_equipipo y pasamos equipo a buscar
                buscar_equipo(driver, equipoo)
                # Llamamos al metodo extraer_resultados y los resultados dataframe los asignamos a una variable df_resultados
                df_resultados = extraer_resultados(driver, str(agno+1))
                url_actual = driver.current_url
                nueva_url = cambiar_agno_url(str(agno),url_actual)
                driver.get(nueva_url)
            else:
                agno = '2023'
                df_resultados = extraer_resultados(driver, agno)
            # Retornamos el data frame
            return df_resultados
        except WebDriverException as e:
            print(f'Error al cargar la pagina o interactuar con el WebDriver: {e}')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

def entrar_a_pag_resultados_2(driver, equipo, agnos=None):
    try:
        df_resultados = []
        # Llamamos al metodo buscar_equipipo y pasamos equipo a buscar
        buscar_equipo(driver, equipo)
        if agnos:
            for i, agno in enumerate(agnos):
                    url_actual = driver.current_url
                    if i == 0:
                        nueva_url = cambiar_agno_url(str(agno),url_actual)
                    else:
                        nueva_url = cambiar_ultimo_segmento(str(agno),url_actual)
                    driver.get(nueva_url)
                    # Llamamos al metodo extraer_resultados y los resultados dataframe los asignamos a una variable df_resultados
                    df_resultados.append(extraer_resultados(driver, agno))  
            df_resultados = pd.concat(df_resultados,ignore_index=True)                 
            print(f'Estas son todas las temporadas a imprimir: {len(agnos)}')
            return df_resultados
        else:
            df_resultados.append(extraer_resultados(driver, datetime.date.today().year))
            df_resultados = pd.concat(df_resultados,ignore_index=True) 
            print(f'Estas son todas las temporadas a imprimir: 1')
            return df_resultados
    except WebDriverException as e:
        print(f'Error al cargar la pagina o interactuar con el WebDriver: {e}')
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")