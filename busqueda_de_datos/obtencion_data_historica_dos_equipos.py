import pandas as pd
from busqueda_datos_espn import entrar_a_pag_resultados_2, driver_quit, inicializar_driver
import pandas as pd
'''
Fabian Israel Aguirre Mancillas 07/08/24
Parte numero 2.0
'''
def obtencion_data_historica_dos_equipos(equipo_home, equipo_away, *agnos):
    driver = inicializar_driver()
    equipos = [equipo_home,equipo_away]
    df_equipos = []
    for contador, equipo in enumerate(equipos):
            print(f'Procesando equipo Home: {contador + 1}/{len(equipos)}: {equipo}')
            resultado = entrar_a_pag_resultados_2(driver, equipo, *agnos)
            if resultado is not None:
                df_equipos.extend(resultado)
    
    #driver_quit()

    df_equipos = pd.concat(df_equipos, ignore_index=True)
    df_equipos.to_csv('data_historica_versus.csv', index=False)
    return df_equipos