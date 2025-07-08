''' INFO
Define a interpolação dos pontos e categoriza cada tipo de combinação de argumentos para gerar os gráficos.
'''

import numpy as np
from scipy.interpolate import make_interp_spline
from .criacao_grafico import criacao_grafico

def iteracao_grafico(dicionario_argumentos, axs, ling_graf, e = None):

  df = dicionario_argumentos['df']
  variavel = dicionario_argumentos['variavel']
  componente_velocidade = dicionario_argumentos['componente_velocidade']
  estacao = dicionario_argumentos['estacao']
  modo = dicionario_argumentos['modo']
  plataforma = dicionario_argumentos['plataforma']
  data = dicionario_argumentos['data']
  ano = dicionario_argumentos['ano']

  # Loop para fazer um gráfico para cada estação do ano
  if estacao == "Todas":
    for e, est in enumerate(["Verão", "Outono", "Inverno", "Primavera"]):
      df_estacao = df[df['Estação_do_Ano'] == est].copy()
      dicionario_argumentos['df'] = df_estacao
      dicionario_argumentos['estacao'] = est
      iteracao_grafico(dicionario_argumentos, axs, ling_graf, e)
    return # A execução da função é interrompida aqui
  else:
    pass


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

      if modo == 'Original':
        if e == None: # Ou seja, se estacao != Todas
          m = 0
        else:
          m = e
        # Cria o gráfico para os dados originais de velocidade do vento
        criacao_grafico(axs[m], cores[c], Y, X_velocidade, Y_smooth, X_smooth_velocidade, 'original', plataforma, estacao, horario, 'velocidade', componente_velocidade, data, ano, ling_graf)

      elif modo == 'Original-Derivada':
        m = 0
        n = 1

        # Cria o gráfico para os dados originais de velocidade do vento
        criacao_grafico(axs[m], cores[c], Y, X_velocidade, Y_smooth, X_smooth_velocidade, 'original', plataforma, estacao, horario, 'velocidade', componente_velocidade, data, ano, ling_graf)
        # Cria o gráfico para a derivada da velocidade do vento
        criacao_grafico(axs[n], cores[c], Y, X_velocidade, Y_smooth, X_smooth_velocidade, 'derivada', plataforma, estacao, horario, 'velocidade', componente_velocidade, data, ano, ling_graf)


    # Verifica se o modo inclui a temperatura ('temperatura' ou 'ambos')
    if variavel in ['Temperatura', 'Ambas']:

      # Coluna de temperatura para o eixo X do gráfico
      X_temperatura = df_hora['Temperatura_C']
      # Interpolação suave dos valores de temperatura em relação aos valores suavizados de altura
      X_smooth_temperatura = make_interp_spline(Y, X_temperatura)(Y_smooth)

      # Verifica se o tipo de gráfico solicitado é 'original' ou 'derivada'
      if modo == 'Original':
        if e == None: # Ou seja, se estacao != Todas
          if variavel == 'Ambas':
            m = 1
          elif variavel == 'Temperatura':
            m = 0

        else:
          m = e

        # Cria o gráfico para os dados originais de temperatura
        criacao_grafico(axs[m], cores[c], Y, X_temperatura, Y_smooth, X_smooth_temperatura, 'original', plataforma, estacao, horario, 'temperatura', componente_velocidade, data, ano, ling_graf)

      # Caso o tipo seja 'ambos' (original e derivada), cria dois gráficos: um para os dados originais e outro para a derivada
      elif modo == 'Original-Derivada':
        # Sempre variavel = Temperatura
        m = 0
        n = 1


        # Cria o gráfico para os dados originais de temperatura
        criacao_grafico(axs[m], cores[c], Y, X_temperatura, Y_smooth, X_smooth_temperatura, 'original', plataforma, estacao, horario, 'temperatura', componente_velocidade, data, ano, ling_graf)
        # Cria o gráfico para a derivada da temperatura
        criacao_grafico(axs[n], cores[c], Y, X_temperatura, Y_smooth, X_smooth_temperatura, 'derivada', plataforma, estacao, horario, 'temperatura', componente_velocidade, data, ano, ling_graf)

