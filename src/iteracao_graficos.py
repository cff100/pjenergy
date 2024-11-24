import numpy as np
from scipy.interpolate import make_interp_spline

def iteracao_grafico(dicionario_argumentos):

  df = dicionario_argumentos['df']
  variavel = dicionario_argumentos['variavel']
  componente_velocidade = dicionario_argumentos['componente_velocidade']
  estacao = dicionario_argumentos['estacao']

  # Lista de horários únicos no DataFrame
  horarios = list(df['Horário_Brasília'].unique())

  # Lista de cores para os gráficos, onde cada cor será usada para horários diferentes
  cores = ['blue', 'green', 'red', 'purple']

  # Loop para iterar pelos horários definidos
  for c, horario in enumerate(horarios):

    # Filtra dados para o horário específico
    df_hora = df[df['Horário_Brasília'] == horario]
    # Ordena os dados filtrados pela coluna que contém as alturas, garantindo que os valores de altura estejam em ordem crescente
    df_hora = df_hora.sort_values('Altitude_m')
    df_hora = df_hora.reset_index(drop=True)

    print(df_hora)

    if estacao == "Todas":
      for est in ["Verão", "Outono", "Inverno", "Primavera"]:
        df_hora_estacao = df_hora[df_hora['Estação_do_Ano'] == est]
        dicionario_argumentos['df'] = df_hora_estacao
        dicionario_argumentos['estacao'] = est
        X_smooth_velocidade, Y_smooth, cores[c] = iteracao_grafico(dicionario_argumentos)
      return X_smooth_velocidade, Y_smooth, cores[c]

    # Coluna de alturas para o eixo Y do gráfico
    Y = df_hora['Altitude_m']
    # Gera uma sequência de valores suavizados para Y, a ser usada para interpolação nos gráficos
    Y_smooth = np.linspace(Y.min(), Y.max(), 400)


    # Verifica se o modo inclui a velocidade do vento ('velocidade' ou 'ambos')
    if variavel in ['Velocidade', 'Ambas']:

      if componente_velocidade == 'u':
        nome_velocidade_vento = 'Velocidade_Vento_u_m/s'
      elif componente_velocidade == 'v':
        nome_velocidade_vento = 'Velocidade_Vento_v_m/s'
      elif componente_velocidade == 'Resultante':
        nome_velocidade_vento = 'Velocidade_Vento_resultante_m/s'

      # Coluna de velocidade do vento para o eixo X do gráfico
      X_velocidade = df_hora[nome_velocidade_vento]
      # Interpolação suave dos valores de velocidade do vento em relação aos valores suavizados de altura
      X_smooth_velocidade = make_interp_spline(Y, X_velocidade)(Y_smooth)

      return X_smooth_velocidade, Y_smooth, cores[c]
