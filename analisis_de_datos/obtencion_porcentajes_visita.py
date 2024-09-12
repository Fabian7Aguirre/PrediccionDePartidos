import pandas as pd
from analisis_de_datos.obtencion_porcentajes_casa import equipo_filtrado
'''
Fabian Israel Aguirre Mancillas 07/08/24
Parte numero 5
'''

def porcent_victoria_visita(df_equipo_filtrado, victorias_visita, total_partidos_visita):
    '''
    Calcular el Porcentaje de Victorias en Visita
    El porcentaje de victorias en visita se calcula dividiendo el número de victorias en visita 
    por el número total de partidos jugados en visita y multiplicándolo por 100.

    Porcentaje de victorias en visita = (victorias en visita / total de partidos en visita) x 100
    '''
    # "porcentaje de victorias en visita"
    # Verificar si el denominador es cero
    total_partidos = len(df_equipo_filtrado[total_partidos_visita])
    victorias = len(df_equipo_filtrado[victorias_visita])
    if total_partidos == 0:
        porcent_victoria_visita = 0
    else:
        porcent_victoria_visita = round((victorias / total_partidos) * 100, 2)
    if porcent_victoria_visita >= 70:
        rendimiento = 'Excelente'
        puntaje = 4
    elif porcent_victoria_visita >= 50 and porcent_victoria_visita <= 69:
        rendimiento = 'Bueno'
        puntaje = 3
    elif porcent_victoria_visita >= 30 and porcent_victoria_visita <= 49:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return float(porcent_victoria_visita), rendimiento, puntaje

def prom_goles_marcados_visita(df_equipo_filtrado, total_partidos_visita):
    '''
        Promedio de goles marcados en visita
        Promedio de goles marcados en visita: Divide el total de goles marcados en visita por el número de partidos jugados en visita.
    '''
    # Verificar si el denominador es cero
    total_partidos = len(df_equipo_filtrado[total_partidos_visita])
    total_goles = df_equipo_filtrado[total_partidos_visita]['Goles Away'].sum()
    if total_partidos == 0:
        prom_goles_marcados_visita = 0
    else:
        prom_goles_marcados_visita = round((total_goles / total_partidos), 2)
    if prom_goles_marcados_visita >= 2.5:
        rendimiento = 'Excelente'
        puntaje = 4
    elif prom_goles_marcados_visita >= 1.5 and prom_goles_marcados_visita <= 2.4:
        puntaje = 3
        rendimiento = 'Bueno'
    elif prom_goles_marcados_visita >= 0.8 and prom_goles_marcados_visita <= 1.4:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return float(prom_goles_marcados_visita), rendimiento, puntaje

def prom_goles_concedidos_visita(df_equipo_filtrado, total_partidos_visita):
    '''
        Promedio de goles concedidos en visita
        Divide el total de goles concedidos en visita entre el total de partidos jugados en visita
    '''
    # Verificar si el denominador es cero
    total_partidos = len(df_equipo_filtrado[total_partidos_visita])
    total_goles = df_equipo_filtrado[total_partidos_visita]['Goles Home'].sum()
    if total_partidos == 0:
        prom_goles_concedidos_visita = 0
    else:
        prom_goles_concedidos_visita = round((total_goles / total_partidos), 2)
    if prom_goles_concedidos_visita < 0.5:
        rendimiento = 'Excelente'
        puntaje = 4
    elif prom_goles_concedidos_visita >= 0.5 and prom_goles_concedidos_visita <= 1:
        rendimiento = 'Bueno'
        puntaje = 3
    elif prom_goles_concedidos_visita >= 1.1 and prom_goles_concedidos_visita <= 1.5:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return float(prom_goles_concedidos_visita), rendimiento, puntaje

def dif_goles_visita(df_equipo_filtrado, total_partidos_visita):
    '''
        Diferencia de goles en visita
        La diferencia de goles es la resta entre los goles marcados y los goles concedidos.
        Diferencia de goles en visita = Total de goles marcados en visita - Total de goles concedidos en visita 
    '''
    dif_goles_visita = df_equipo_filtrado[total_partidos_visita]['Goles Away'].sum()-df_equipo_filtrado[total_partidos_visita]['Goles Home'].sum()
    if dif_goles_visita > 15:
        rendimiento = 'Excelente'
        puntaje = 4
    elif dif_goles_visita >= 7 and dif_goles_visita <= 14:
        rendimiento = 'Bueno'
        puntaje = 3
    elif dif_goles_visita >= 0 and dif_goles_visita <= 6:
        rendimiento = 'Regular'
        puntaje = 2
    else:
        rendimiento = 'Pobre'
        puntaje = 1
    return float(dif_goles_visita), rendimiento, puntaje

'''
1. Porcentaje de Victorias en Visita

    Excelente: 70% o más
    
    Bueno: 50% - 69%

    Regular: 30% - 49%
    
    Pobre: Menos del 30%
2. Promedio de Goles Marcados en Visita
    Excelente: 2.5 goles por partido o más

    Bueno: 1.5 - 2.4 goles por partido

    Regular: 0.8 - 1.4 goles por partido

    Pobre: Menos de 0.8 goles por partido

3. Promedio de Goles Concedidos en Visita
    Excelente: Menos de 0.5 goles por partido

    Bueno: 0.5 - 1.0 goles por partido

    Regular: 1.1 - 1.5 goles por partido

    Pobre: Más de 1.5 goles por partido

4. Diferencia de Goles en Visita
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

def puntuacon_general(pvv, pgmv, pgcv, dgv):
    '''
        Ahora tenemos 4 resultados para observar cuando el equipo juega en casa
        porcent_victoria_casa, prom_goles_marcados_casa, prom_goles_concedidos_casa, dif_goles_casa
    '''
    puntuacon_general = (pvv[2] * 0.35) + (pgmv[2] * 0.25) + (pgcv[2] * 0.20) + (dgv[2] * 0.20)
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
    

def lanzar_puntuación_general_visita(equipo):
    #Abrimos archivo  y los asignamos a un dataframe
    # Agregamos el parametro encoding='utf-8 para que pueda leer todos los caracteres del archivo
    with open('clean_data_historica_versus.csv', 'r', encoding='utf-8') as file:
        df_clean_data = pd.read_csv(file)

    # Obtenemos dataframe solo de este equipo
    df_equipo_filtrado = equipo_filtrado(equipo, df_clean_data)
    # "total empates"
    total_empates = df_equipo_filtrado['Away'].str.contains(equipo) & (df_equipo_filtrado['Goles Home'] == df_equipo_filtrado['Goles Away'])
    # "victorias en casa"
    victorias_visita = df_equipo_filtrado['Away'].str.contains(equipo) & (df_equipo_filtrado['Goles Away'] > df_equipo_filtrado['Goles Home'])
    # "total de partidos en casa"
    total_partidos_visita = df_equipo_filtrado['Away'].str.contains(equipo)

    pvv = (porcent_victoria_visita(df_equipo_filtrado, victorias_visita, total_partidos_visita))
    pgmv = prom_goles_marcados_visita(df_equipo_filtrado, total_partidos_visita)
    pgcv = prom_goles_concedidos_visita(df_equipo_filtrado, total_partidos_visita)
    dgv = dif_goles_visita(df_equipo_filtrado, total_partidos_visita)

    dict_analisis = {'Equipo': equipo, '% Victorias en Visita': pvv, 'x̅ + Goles en Visita':pgmv, 'x̅ -Goles en Visita':pgcv, 'Diferencia en Visita +/- G':dgv, 'Puntuacion General %': puntuacon_general(pvv, pgmv, pgcv, dgv)}
    #conclucion = f"Porcentaje de victorias en visita: {pvv}\nPromedio de goles marcados en visita: {pgmv}\nPromedio de goles concedidos en visita: {pgcv}\nDiferencia total de goles en visita: {dgv}"

    return dict_analisis
