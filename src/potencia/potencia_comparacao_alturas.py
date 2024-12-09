import pjenergy.main as mp
import pandas as pd
from scipy.integrate import simps

def potencia_altura(perguntas, l_vel_inf, l_vel_sup, plotar_graficos):

  # Parâmetros iniciais
  rho = 1.225  # Densidade do ar (kg/m^3)
  A = 1       # Área da unitária da turbina (m^2)

  df_mestre_limitado = pd.DataFrame()

  for an in range(2021, 2024):
    for est in ['Verão', 'Outono', 'Inverno', 'Primavera']:
      df_mestre_limitado = pd.concat([df_mestre_limitado, mp.pot(perguntas = False, pressao = 'Todas', estacao = est, ano = an, horario = 'Todos', plotar_graficos = plotar_graficos)])
  print(f'df_mestre_limitado: {df_mestre_limitado}')

  for idx, df in enumerate(df_mestre_limitado['Dataframe_Probabilidade']):

    if not isinstance(df, pd.DataFrame):
      print(f"Aviso: Elemento no índice {idx} não é um DataFrame (df: {df}), pulando...")
      continue

    df_limitado = df.loc[
        (df['Velocidade_Vento_resultante_m/s'] >= l_vel_inf) &
        (df['Velocidade_Vento_resultante_m/s'] <= l_vel_sup)
    ]

    print(f'Índice: {idx} - df_limitado: {df_limitado}')

    # Calcular a potência
    df_limitado['Potência'] = 0.5 * rho * A * (df_limitado['Velocidade_Vento_resultante_m/s'] ** 3) / 10**3  # Em kW
    # Calcular a potência ponderada
    df_limitado['Potência_Ponderada'] = df_limitado['Potência'] * df_limitado['Densidade_de_Probabilidade']

    df_limitado = df_limitado.sort_values(by='Velocidade_Vento_resultante_m/s')

    #print(f'df_limitado: {df_limitado}')

    df_mestre_limitado.at[idx, 'Dataframe_Probabilidade'] = df_limitado

    potencia_media_local = simps(df_limitado['Potência_Ponderada'], df_limitado['Velocidade_Vento_resultante_m/s'])

    df_mestre_limitado.loc[idx, 'Potência_Média'] = potencia_media_local

    df_mestre_limitado.loc[idx, 'Altitude'] = df_limitado['Altitude_m'].iloc[0]

  print(f'df_mestre_limitado: {df_mestre_agrupado}')

  df_mestre_limitado.groupby('Pressão')

  colunas_relevantes = ['Pressão', 'Altitude', 'Potência_Média']
  df_mestre_limitado = df_mestre_limitado[colunas_relevantes]

  df_mestre_agrupado = df_mestre_limitado.groupby('Pressão').agg({'Altitude': 'first', 'Potência_Média': 'sum'}).reset_index()
  df_mestre_agrupado = df_mestre_agrupado.sort_values(by='Altitude')

  print(df_mestre_agrupado)