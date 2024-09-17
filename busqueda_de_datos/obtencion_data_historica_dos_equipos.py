import pandas as pd
from busqueda_de_datos.busqueda_datos_espn import entrar_a_pag_resultados, driver_quit
import pandas as pd
'''
Fabian Israel Aguirre Mancillas 07/08/24
Parte numero 2.0
'''
def obtencion_data_historica_dos_equipos(equipo_home, equipo_away):
    equipos = [equipo_home,equipo_away]
    df_equipos = []
    for contador, equipo in enumerate(equipos):
            bandera = True
            print(f'Procesando equipo Home: {contador + 1}/{len(equipos)}: {equipo}')
            resultado = entrar_a_pag_resultados(equipo, bandera)
            if resultado is not None:
                df_equipos.append(resultado)
            bandera = False
            resultado = entrar_a_pag_resultados(equipo, bandera)
            if resultado is not None:
                df_equipos.append(resultado)
    
    #driver_quit()

    df_equipos = pd.concat(df_equipos, ignore_index=True)
    df_equipos.to_csv('data_historica_versus.csv', index=False)
    return df_equipos