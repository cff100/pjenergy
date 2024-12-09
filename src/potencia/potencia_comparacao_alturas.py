import pjenergy.main as mp
import pandas as pd

def potencia_altura(perguntas, l_vel_inf, l_vel_sup):

  for an in range(2021, 2024):
    for est in ['Verão', 'Outono', 'Inverno', 'Primavera']:
      df_mestre = pd.concat([df_mestre, mp.pot(perguntas = False, pressao = 'Todas', estacao = est, ano = an, horario = 'Todos')])

  '''potencia_media = simps(df['Potência_Ponderada'], df['Velocidade_Vento_resultante_m/s'])
  df_mestre.loc[idx, 'Potência_Média'] = potencia_media
  print(f'Potência Ponderada Média: {potencia_media} kW/m^2')

  #print(df_mestre['Dataframe_Probabilidade'][0]['Velocidade_Vento_resultante_m/s'])
  potencia_media_total = df_mestre['Potência_Média'].sum()
  print(f'Potência Total: {potencia_media_total} kW/m^2')'''

  print(df_mestre)