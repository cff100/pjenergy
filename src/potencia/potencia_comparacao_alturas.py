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

  for idx, df in enumerate(df_mestre_limitado['Dataframe_Probabilidade']):

    if not isinstance(df, pd.DataFrame):
      print(f"Aviso: Elemento no índice {idx} não é um DataFrame, pulando...")
      continue

    df = df.loc[
        (df['Velocidade_Vento_resultante_m/s'] >= l_vel_inf) &
        (df['Velocidade_Vento_resultante_m/s'] <= l_vel_sup)
    ]

    # Calcular a potência
    df['Potência'] = 0.5 * rho * A * (df['Velocidade_Vento_resultante_m/s'] ** 3) / 10**3  # Em kW
    # Calcular a potência ponderada
    df['Potência_Ponderada'] = df['Potência'] * df['Densidade_de_Probabilidade']

    df = df.sort_values(by='Velocidade_Vento_resultante_m/s')

    df_mestre_limitado.at[idx, 'Dataframe_Probabilidade'] = df

    potencia_media_local = simps(df['Potência_Ponderada'], df['Velocidade_Vento_resultante_m/s'])

    df_mestre_limitado.loc[idx, 'Potência_Média'] = potencia_media_local

    df_mestre_limitado.loc[idx, 'Altitude'] = df['Altitude_m'].iloc[0]

  df_mestre_limitado.groupby('Pressão')

  colunas_relevantes = ['Pressão', 'Altitude', 'Potência_Média']
  df_mestre_limitado = df_mestre_limitado[colunas_relevantes]

  df_mestre_agrupado = df_mestre_limitado.groupby('Pressão').agg({'Altitude': 'first', 'Potência_Média': 'sum'}).reset_index()
  df_mestre_agrupado = df_mestre_agrupado.sort_values(by='Altitude')

  print(df_mestre_agrupado)