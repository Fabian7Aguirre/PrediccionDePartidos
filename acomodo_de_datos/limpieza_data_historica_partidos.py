import pandas as pd
import pickle

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
        puntos_h.append((int(split_h[0])*3) + int(split_h[1]))
        puntos_a.append((int(split_a[0])*3) + int(split_a[1]))
        

    df_partidos['Pts-H'] = puntos_h
    df_partidos['Pts-A'] = puntos_a

    return df_partidos

def agregar_racha(df_partidos):
    # Concatenamos los ids de casa y visita
    df_ids = pd.DataFrame(pd.concat([df_partidos['id_H'], df_partidos['id_A']], ignore_index=True))
    df_ids.rename(columns={0:'ID'}, inplace=True)
    # Eliminamos duplicados
    df_ids.drop_duplicates(inplace=True, ignore_index=True)
    # Creamos columna de racha
    df_ids['Racha'] = 0
    df_partidos['Racha-H'] = 0
    df_partidos['Racha-A'] = 0
    df_partidos.sort_values(by='Fecha', ascending=True,ignore_index=True, inplace=True)

    for i, row in df_partidos.iterrows():
        if(int(row['H-Score']) > int(row['A-Score'])):
            # Encontrar las filas donde la columna 'id' tiene el mismo 'id' y cambiar el valor de la columna 'Racha'
            # Si Home gana le sumamos 1 punto a la racha en el dataframe de ids 'df_ids'
            # A Away lo cambiamos a 0 ya que se acabo su racha
            # Ahora guardamos la racha de Home en la fila que estamos iterando
            df_ids.loc[df_ids['ID'] == row['id_H'], 'Racha'] += 1
            df_ids.loc[df_ids['ID'] == row['id_A'], 'Racha'] = 0   
            racha_H = df_ids.loc[df_ids['ID'] == row['id_H'], 'Racha'].values[0]
            # Cambiar el valor a la racha asignando el valor guardado en df_ids
            df_partidos.at[i, 'Racha-H'] = racha_H
        elif(int(row['H-Score']) < int(row['A-Score'])):
            # Encontrar las filas donde la columna 'id' tiene el mismo 'id' y cambiar el valor de la columna 'Racha'
            # Si Away gana le sumamos 1 punto a la racha en el dataframe de ids 'df_ids'
            # A Home lo cambiamos a 0 ya que se acabo su racha
            # Ahora guardamos la racha de Away en la fila que estamos iterando
            df_ids.loc[df_ids['ID'] == row['id_A'], 'Racha'] += 1
            df_ids.loc[df_ids['ID'] == row['id_H'], 'Racha'] = 0
            racha_A = df_ids.loc[df_ids['ID'] == row['id_A'], 'Racha'].values[0]
            # Cambiar el valor a la racha asignando el valor guardado en df_ids
            df_partidos.at[i, 'Racha-A'] = racha_A
        else:
            df_ids.loc[df_ids['ID'] == row['id_H'], 'Racha'] = 0
            df_ids.loc[df_ids['ID'] == row['id_A'], 'Racha'] = 0 
            
    
    return df_partidos

def guardar_df(nombre_df, df_tabla):
    try:
            with open(nombre_df, 'wb') as output:
                pickle.dump(df_tabla, output)
            df_tabla.to_csv(nombre_df+'.csv', index=False)
    except FileExistsError:
        print('El archivo no existe.')
    except IOError:
        print("Error de entrada/salida.")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

def limpiar_df():
    df_partidos = cargar_bd()

    df_partidos = agregar_pts(df_partidos)

    df_partidos = agregar_racha(df_partidos)

    guardar_df('Clean_data_historica_LMX24', df_partidos)

    return df_partidos

limpiar_df()


#print(df_partidos[(df_partidos['Home'].str.contains('Toluca')) | (df_partidos['Away'].str.contains('Toluca'))])
#print(df_partidos[df_partidos['Home'].str.contains('Queretaro')])