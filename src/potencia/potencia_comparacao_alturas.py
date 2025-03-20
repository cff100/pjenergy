import main as mp
import pandas as pd
#from scipy.integrate import simps
import scipy.integrate
import matplotlib.pyplot as plt

def potencia_altura(perguntas, l_vel_inf, l_vel_sup, plotar_graficos):

  # Parâmetros iniciais
  rho = 1.225  # Densidade do ar (kg/m^3)
  A = 1       # Área da unitária da turbina (m^2)

  df_mestre_limitado = pd.DataFrame()

  anos = [2021, 2022, 2023]

  for an in anos:
    for est in ['Verão', 'Outono', 'Inverno', 'Primavera']:
      df_mestre_limitado = pd.concat([df_mestre_limitado, mp.pot(perguntas = False, pressao = 'Todas', estacao = est, ano = an, horario = 'Todos', plotar_graficos = plotar_graficos)])

  print(f'1 -> df_mestre_limitado: {df_mestre_limitado}')
  print('\n \n \n')

  # Remover todas as linhas com NaN na coluna 'Dataframe_Probabilidade'
  df_mestre_limitado = df_mestre_limitado.dropna(subset=['Dataframe_Probabilidade'])

  print(f'2 -> df_mestre_limitado: {df_mestre_limitado}')
  print('\n \n \n')

  for idx, df in enumerate(df_mestre_limitado['Dataframe_Probabilidade']):

    print(f'Índice: {idx}')
    print(f'df: {df}')
    print('\n \n \n')

    if not isinstance(df, pd.DataFrame):
      print(f"Aviso: Elemento no índice {idx} não é um DataFrame (df: {df}), pulando...")
      print('\n \n \n')
      continue

    df_limitado = df.loc[
        (df['Velocidade_Vento_resultante_m/s'] >= l_vel_inf) &
        (df['Velocidade_Vento_resultante_m/s'] <= l_vel_sup)
    ]

    print(f'Índice: {idx} - df_limitado: {df_limitado}')
    print('\n \n \n')


    # Calcular a potência
    df_limitado['Potência'] = 0.5 * rho * A * (df_limitado['Velocidade_Vento_resultante_m/s'] ** 3) / 10**3  # Em kW
    # Calcular a potência ponderada
    df_limitado['Potência_Ponderada'] = df_limitado['Potência'] * df_limitado['Densidade_de_Probabilidade']

    print(f'3 -> df_limitado: {df_limitado}')
    print('\n \n \n')


    df_limitado = df_limitado.sort_values(by='Velocidade_Vento_resultante_m/s')

    print(f'4 -> df_limitado: {df_limitado}')
    print('\n \n \n')


    df_mestre_limitado.at[idx, 'Dataframe_Probabilidade'] = df_limitado

    print(f'5 -> df_mestre_limitado: {df_mestre_limitado}')
    print('\n \n \n')


    potencia_media_local = scipy.integrate.simps(df_limitado['Potência_Ponderada'], df_limitado['Velocidade_Vento_resultante_m/s'])

    print(f'6 -> potencia_media_local: {potencia_media_local}')
    print('\n \n \n')

    df_mestre_limitado.loc[idx, 'Potência_Média'] = potencia_media_local

    print(f'7 -> df_mestre_limitado: {df_mestre_limitado}')
    print('\n \n \n')

    df_mestre_limitado.loc[idx, 'Altitude'] = df_limitado['Altitude_m'].iloc[0]

    print(f'8 -> df_mestre_limitado: {df_mestre_limitado}')
    print('\n \n \n')

  print(f'9 -> df_mestre_limitado: {df_mestre_limitado}')
  print('\n \n \n')

  df_mestre_limitado.groupby('Pressão')

  print(f'10 -> df_mestre_limitado: {df_mestre_limitado}')
  print('\n \n \n')

  colunas_relevantes = ['Pressão', 'Altitude', 'Potência_Média']
  df_mestre_limitado = df_mestre_limitado[colunas_relevantes]

  df_mestre_agrupado = df_mestre_limitado.groupby('Pressão').agg({'Altitude': 'first', 'Potência_Média': 'sum'}).reset_index()

  print(f'11 -> df_mestre_agrupado: {df_mestre_agrupado}')
  print('\n \n \n')

  df_mestre_agrupado = df_mestre_agrupado.sort_values(by='Altitude')

  print(f'12 -> df_mestre_agrupado: {df_mestre_agrupado}')
  print('\n \n \n')

  df_mestre_agrupado['Potência_Média'] = df_mestre_agrupado['Potência_Média'] / len(anos)  # Dividido pelo número de anos para uma média anual
  
  print(f'13 -> df_mestre_agrupado: {df_mestre_agrupado}')
  print('\n \n \n')


  # Configurar o gráfico
  plt.figure(figsize=(10, 6))
  plt.plot(
      df_mestre_agrupado['Altitude'],
      df_mestre_agrupado['Potência_Média'],
      marker='o',
      linestyle='-',
      color='b',
      label='Potência Média'
  )

  # Configurações adicionais
  plt.title('Potência Média Anual x Altura', fontsize=14)
  plt.xlabel('Altura (m)', fontsize=12)
  plt.ylabel('Potência Média Anual (kW/m^2)', fontsize=12)
  plt.grid(True, linestyle='--', alpha=0.7)
  plt.legend(fontsize=12)
  plt.tight_layout()

  # Mostrar o gráfico
  plt.show()
