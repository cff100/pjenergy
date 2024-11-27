def dataframe_media(df, estacoes_separadas):
  if estacoes_separadas == True:
    categorias_agrupar = ['Estação_do_Ano', 'Altitude_m', 'Horário_Brasília']
    colunas_ordem = ['Nível_de_Pressão_hPa', 'Altitude_m', 'Estação_do_Ano',
                     'Horário_Brasília', 'Horário_UTC', 'Velocidade_Vento_u_m/s',
                     'Velocidade_Vento_v_m/s', 'Velocidade_Vento_resultante_m/s', 'Temperatura_K', 'Temperatura_C']

    df_media = df.groupby(categorias_agrupar).agg({
    'Velocidade_Vento_resultante_m/s': 'mean',
    'Velocidade_Vento_u_m/s': 'mean',
    'Velocidade_Vento_v_m/s': 'mean',
    'Temperatura_K': 'mean',
    'Temperatura_C': 'mean',
    'Nível_de_Pressão_hPa': 'first',
    'Horário_UTC': 'first'
    }).reset_index()

  else:
    categorias_agrupar = ['Altitude_m', 'Horário_Brasília']
    colunas_ordem = ['Nível_de_Pressão_hPa', 'Altitude_m', 'Estação_do_Ano',
                     'Horário_Brasília', 'Horário_UTC', 'Velocidade_Vento_u_m/s',
                     'Velocidade_Vento_v_m/s', 'Velocidade_Vento_resultante_m/s', 'Temperatura_K', 'Temperatura_C']

    df_media = df.groupby(categorias_agrupar).agg({
    'Velocidade_Vento_resultante_m/s': 'mean',
    'Velocidade_Vento_u_m/s': 'mean',
    'Velocidade_Vento_v_m/s': 'mean',
    'Temperatura_K': 'mean',
    'Temperatura_C': 'mean',
    'Nível_de_Pressão_hPa': 'first',
    'Horário_UTC': 'first',
    'Estação_do_Ano': 'first'
    }).reset_index()


  return df_media[colunas_ordem]
