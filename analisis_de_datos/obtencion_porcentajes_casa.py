import pandas as pd
'''
Fabian Israel Aguirre Mancillas 07/08/24
Parte numero 4
'''

def equipo_filtrado(equipo, df_clean_data):
    '''
        Creamos un dataframe donde solo contenga el equipo que recibio como parametro, ya sea como 'Home' o 'Away'
    '''
    filtro = df_clean_data['Home'].str.contains(equipo) | df_clean_data['Away'].str.contains(equipo)
    df_equipo_filtrado = df_clean_data[filtro]
    return df_equipo_filtrado


'''# Equipo que analizaremos
#equipo = 'Tigres UANL'
# Obtenemos dataframe solo de este equipo
df_equipo_filtrado = equipo_filtrado(equipo, df_clean_data)
# "total empates"
total_empates = df_equipo_filtrado['Home'].str.contains(equipo) & (df_equipo_filtrado['Goles Home'] == df_equipo_filtrado['Goles Away'])
# "victorias en casa"
victorias_casa = df_equipo_filtrado['Home'].str.contains(equipo) & (df_equipo_filtrado['Goles Home'] > df_equipo_filtrado['Goles Away'])
# "total de partidos en casa"
total_partidos_casa = df_equipo_filtrado['Home'].str.contains(equipo)'''


def porcent_victoria_casa(df_equipo_filtrado, victorias_casa, total_partidos_casa):
    '''
    Calcular el Porcentaje de Victorias en Casa
    El porcentaje de victorias en casa se calcula dividiendo el número de victorias en casa 
    por el número total de partidos jugados en casa y multiplicándolo por 100.

    Porcentaje de victorias en casa = (victorias en casa / total de partidos en casa) x 100
    '''
    # "porcentaje de victorias en casa"
    # Verificar si el denominador es cero
    total_partidos = len(df_equipo_filtrado[total_partidos_casa])
    victorias = len(df_equipo_filtrado[victorias_casa])

    if total_partidos == 0:
        porcent_victoria_casa = 0
    else:
        porcent_victoria_casa = round((victorias / total_partidos) * 100, 2)
    if porcent_victoria_casa >= 70:
        rendimiento = 'Excelente'
        puntaje = 4
    elif porcent_victoria_casa >= 50 and porcent_victoria_casa <= 69:
        rendimiento = 'Bueno'
        puntaje = 3
    elif porcent_victoria_casa >= 30 and porcent_victoria_casa <= 49:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return float(porcent_victoria_casa), rendimiento, puntaje


def prom_goles_marcados_casa(df_equipo_filtrado, total_partidos_casa):
    '''
        Promedio de goles marcados en casa
        Promedio de goles marcados en casa: Divide el total de goles marcados en casa por el número de partidos jugados en casa.
    '''
    # Verificar si el denominador es cero
    total_goles = df_equipo_filtrado[total_partidos_casa]['Goles Home'].sum()
    total_partidos = len(df_equipo_filtrado[total_partidos_casa])

    if total_partidos == 0:
        prom_goles_marcados_casa = 0
    else:
        prom_goles_marcados_casa = round((total_goles / total_partidos),2)
    #prom_goles_marcados_casa = round((df_equipo_filtrado[total_partidos_casa]['Goles Home'].sum())/len(df_equipo_filtrado[total_partidos_casa]),2)
    if prom_goles_marcados_casa >= 2.5:
        rendimiento = 'Excelente'
        puntaje = 4
    elif prom_goles_marcados_casa >= 1.5 and prom_goles_marcados_casa <= 2.4:
        puntaje = 3
        rendimiento = 'Bueno'
    elif prom_goles_marcados_casa >= 0.8 and prom_goles_marcados_casa <= 1.4:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return float(prom_goles_marcados_casa), rendimiento, puntaje


def prom_goles_concedidos_casa(df_equipo_filtrado, total_partidos_casa):
    '''
        Promedio de goles concedidos en casa
        Divide el total de goles concedidos en casa entre el total de partidos jugados en casa
    '''
    total_goles = df_equipo_filtrado[total_partidos_casa]['Goles Away'].sum()
    total_partidos = len(df_equipo_filtrado[total_partidos_casa])

    if total_partidos == 0:
        prom_goles_concedidos_casa = 0
    else:
        prom_goles_concedidos_casa = round((total_goles/total_partidos),2)
    #prom_goles_concedidos_casa = round((df_equipo_filtrado[total_partidos_casa]['Goles Away'].sum())/len(df_equipo_filtrado[total_partidos_casa]),2)
    if prom_goles_concedidos_casa < 0.5:
        rendimiento = 'Excelente'
        puntaje = 4
    elif prom_goles_concedidos_casa >= 0.5 and prom_goles_concedidos_casa <= 1:
        rendimiento = 'Bueno'
        puntaje = 3
    elif prom_goles_concedidos_casa >= 1.1 and prom_goles_concedidos_casa <= 1.5:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return float(prom_goles_concedidos_casa), rendimiento, puntaje

def dif_goles_casa(df_equipo_filtrado, total_partidos_casa):
    '''
        Diferencia de goles en casa
        La diferencia de goles es la resta entre los goles marcados y los goles concedidos.
        Diferencia de goles en casa = Total de goles marcados en casa - Total de goles concedidos en casa 
    '''
    dif_goles_casa = df_equipo_filtrado[total_partidos_casa]['Goles Home'].sum()-df_equipo_filtrado[total_partidos_casa]['Goles Away'].sum()
    if dif_goles_casa >= 15:
        rendimiento = 'Excelente'
        puntaje = 4
    elif dif_goles_casa >= 7 and dif_goles_casa <= 14:
        rendimiento = 'Bueno'
        puntaje = 3
    elif dif_goles_casa >= 0 and dif_goles_casa <= 6:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return float(dif_goles_casa), rendimiento, puntaje

'''
1. Porcentaje de Victorias en Casa

    Excelente: 70% o más
    
    Bueno: 50% - 69%

    Regular: 30% - 49%
    
    Pobre: Menos del 30%
2. Promedio de Goles Marcados en Casa
    Excelente: 2.5 goles por partido o más

    Bueno: 1.5 - 2.4 goles por partido

    Regular: 0.8 - 1.4 goles por partido

    Pobre: Menos de 0.8 goles por partido

3. Promedio de Goles Concedidos en Casa
    Excelente: Menos de 0.5 goles por partido

    Bueno: 0.5 - 1.0 goles por partido

    Regular: 1.1 - 1.5 goles por partido

    Pobre: Más de 1.5 goles por partido

4. Diferencia de Goles en Casa
    Excelente: +15 o más

    Bueno: +7 a +14

    Regular: 0 a +6
    
    Pobre: Negativa (menos de 0)




    Excelente: 4 puntos

    Bueno: 3 puntos

    Regular: 2 puntos

    Pobre: 1 punto

    Puntuación general = (Puntuación Métrica 1 x Peso 1) + (Puntuación Métrica 2 x Peso 2) +
    (Puntuación Métrica 3 x Peso 3) + (Puntuación Métrica 4 x Peso 4)

    Porcentaje de Victorias: 35%

    Promedio de Goles Marcados: 25%

    Promedio de Goles Concedidos: 20%

    Diferencia de Goles: 20%
'''


def puntuacon_general(pvc, pgmc, pgcc, dgc):
    '''
        Ahora tenemos 4 resultados para observar cuando el equipo juega en casa
        porcent_victoria_casa, prom_goles_marcados_casa, prom_goles_concedidos_casa, dif_goles_casa
    '''
    
    puntuacon_general = (pvc[2] * 0.35) + (pgmc[2] * 0.25) + (pgcc[2] * 0.20) + (dgc[2] * 0.20)
    puntuacon_general = round((puntuacon_general*100/4),2)
    if puntuacon_general >= 80:
        rendimiento = 'Excelente'
        puntaje = 4
    elif puntuacon_general >= 60 and puntuacon_general <= 79:
        rendimiento = 'Bueno'
        puntaje = 3
    elif puntuacon_general >= 40 and puntuacon_general <= 59:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return puntuacon_general, rendimiento, puntaje
    

def lanzar_puntuación_general_casa(equipo):
    #Abrimos archivo  y los asignamos a un dataframe
    # Agregamos el parametro encoding='utf-8 para que pueda leer todos los caracteres del archivo
    with open('clean_data_historica_versus.csv', 'r', encoding='utf-8') as file:
        df_clean_data = pd.read_csv(file)
    # Obtenemos dataframe solo de este equipo
    df_equipo_filtrado = equipo_filtrado(equipo, df_clean_data)
    # "total empates"
    total_empates = df_equipo_filtrado['Home'].str.contains(equipo) & (df_equipo_filtrado['Goles Home'] == df_equipo_filtrado['Goles Away'])
    # "victorias en casa"
    victorias_casa = df_equipo_filtrado['Home'].str.contains(equipo) & (df_equipo_filtrado['Goles Home'] > df_equipo_filtrado['Goles Away'])
    # "total de partidos en casa"
    total_partidos_casa = df_equipo_filtrado['Home'].str.contains(equipo)

    pvc = (porcent_victoria_casa(df_equipo_filtrado, victorias_casa, total_partidos_casa))
    pgmc = prom_goles_marcados_casa(df_equipo_filtrado, total_partidos_casa)
    pgcc = prom_goles_concedidos_casa(df_equipo_filtrado, total_partidos_casa)
    dgc = dif_goles_casa(df_equipo_filtrado, total_partidos_casa)

    dict_analisis = {'Equipo': equipo, '% Victorias en Casa': pvc, 'x̅ + Goles en Casa':pgmc, 'x̅ - Goles en Casa':pgcc, 'Diferencia en Casa +/- G':dgc, 'Puntuacion General %': puntuacon_general(pvc, pgmc, pgcc, dgc)}

    return dict_analisis