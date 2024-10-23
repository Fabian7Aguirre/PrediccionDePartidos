import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def cargar_bd():
    '''
        Cargamos la base de datos que queremos analisar
    '''
    with open('./Historial_2024_LGM.csv', 'r', encoding='utf-8') as file:
        df_partidos = pd.read_csv(file)
    pd.set_option('display.max_rows', 110)
    df_partidos = df_partidos.drop_duplicates()
    df_partidos = df_partidos.sort_values(by=['Home', 'Fecha'], ascending=[True, False], ignore_index=True)

    return df_partidos

def agregar_pts(df_partidos):
    puntos_h, puntos_a = [], []
    for i, equipo in df_partidos.iterrows():
        split_h = (equipo['H-Record']).split('-')
        split_a = (equipo['A-Record']).split('-')
        puntos_h.append(int(split_h[0]) + int(split_h[1]))
        puntos_a.append(int(split_a[0]) + int(split_a[1]))

        df_partidos['Pts-H'] = puntos_h
        df_partidos['Pts-A'] = puntos_a

        df_partidos
cargar_bd()