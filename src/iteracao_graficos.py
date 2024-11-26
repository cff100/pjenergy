import numpy as np
from scipy.interpolate import make_interp_spline
from .criacao_grafico import criacao_grafico

def iteracao_grafico(dicionario_argumentos, axs, e = None):

  df = dicionario_argumentos['df']
  variavel = dicionario_argumentos['variavel']
  componente_velocidade = dicionario_argumentos['componente_velocidade']
  estacao = dicionario_argumentos['estacao']
  modo = dicionario_argumentos['modo']
  plataforma = dicionario_argumentos['plataforma']
  data = dicionario_argumentos['data']

  print(dicionario_argumentos)

  if estacao == "Todas":
    for e, est in enumerate(["Verão", "Outono", "Inverno", "Primavera"]):
      df_estacao = df[df['Estação_do_Ano'] == est].copy()
      dicionario_argumentos['df'] = df_estacao
      dicionario_argumentos['estacao'] = est
      iteracao_grafico(dicionario_argumentos, axs, e)
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

    print(df_hora)

    # Coluna de alturas para o eixo Y do gráfico
    Y = df_hora['Altitude_m']
    #print(Y)
    
    # Supondo que Y seja o array com as altitudes
    valores_duplicados, contagens = np.unique(Y, return_counts=True)

    # Filtra os valores duplicados (aqueles que aparecem mais de uma vez)
    duplicados = valores_duplicados[contagens > 1]
    contagem_duplicados = contagens[contagens > 1]

    # Exibe os valores duplicados e quantas vezes aparecem
    for val, count in zip(duplicados, contagem_duplicados):
      print(f"Valor duplicado: {val}, Ocorrências: {count}")

    # Gera uma sequência de valores suavizados para Y, a ser usada para interpolação nos gráficos
    Y_smooth = np.linspace(Y.min(), Y.max(), 400)
    print(Y_smooth)


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
        if e == None:
          m = 0
        else:
          m = e
        print(f'm:{m}')
        # Cria o gráfico para os dados originais de velocidade do vento
        criacao_grafico(axs[m], cores[c], Y, X_velocidade, Y_smooth, X_smooth_velocidade, 'original', plataforma, estacao, horario, 'velocidade', componente_velocidade, data)

      elif modo == 'Original-Derivada':
        m = 0
        n = 1
        print(f'm:{m}')
        print(f'n:{n}')

        # Cria o gráfico para os dados originais de velocidade do vento
        criacao_grafico(axs[m], cores[c], Y, X_velocidade, Y_smooth, X_smooth_velocidade, 'original', plataforma, estacao, horario, 'velocidade', componente_velocidade, data)
        # Cria o gráfico para a derivada da velocidade do vento
        criacao_grafico(axs[n], cores[c], Y, X_velocidade, Y_smooth, X_smooth_velocidade, 'derivada', plataforma, estacao, horario, 'velocidade', componente_velocidade, data)



