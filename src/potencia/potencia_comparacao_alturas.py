def potencia_altura(l_vel_inf = 3, l_vel_sup = 24):

  potencia_media = simps(df['Potência_Ponderada'], df['Velocidade_Vento_resultante_m/s'])
  df_mestre.loc[idx, 'Potência_Média'] = potencia_media
  print(f'Potência Ponderada Média: {potencia_media} kW/m^2')

  #print(df_mestre['Dataframe_Probabilidade'][0]['Velocidade_Vento_resultante_m/s'])
  potencia_media_total = df_mestre['Potência_Média'].sum()
  print(f'Potência Total: {potencia_media_total} kW/m^2')