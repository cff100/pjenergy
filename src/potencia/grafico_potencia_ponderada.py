''' INFO
Calcula a potência pondera e cria um gráfico para ela.
'''


import matplotlib.pyplot as plt


def identificacao(pressao_lista, estacao_lista, ano_lista, horario_lista):

  # Todos -> 0, Valor específico -> 1

  if len(pressao_lista) == 1:
    i_pr = 1
  else:
    i_pr = 0

  if len(estacao_lista) == 1:
    i_est = 1
  else:
    i_est = 0

  if len(ano_lista) == 1:
    i_ano = 1
  else:
    i_ano = 0

  if len(horario_lista) == 1:
    i_hor = 1
  else:
    i_hor = 0

  i = [i_pr, i_est, i_ano, i_hor]

  return i







def pond_potencia(df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista):

  # Parâmetros iniciais
  rho = 1.225  # Densidade do ar (kg/m^3)
  A = 1       # Área da unitária da turbina (m^2)

  # Configuração de cores para gráficos
  cores_est = {
  'Verão': 'gold',           # Verão - tom vibrante e ensolarado, representando o calor
  'Outono': 'sienna',        # Outono - tom terroso, sugerindo folhas caindo e clima mais ameno
  'Inverno': 'steelblue',    # Inverno - tom frio, simbolizando o clima mais gelado
  'Primavera': 'mediumseagreen'  # Primavera - tom verde fresco, sugerindo renovação e natureza em flor
  }

  linestyles_est = {
    'Verão': '-',         # Linha contínua para representar o calor constante do verão
    'Outono': '--',       # Linha tracejada, sugerindo a transição e mudanças sutis do outono
    'Inverno': '-.',      # Linha pontilhada e traçada, representando a irregularidade do clima frio
    'Primavera': ':'      # Linha pontilhada fina, simbolizando a leveza da primavera
  }

  # Dicionário atualizado de cores para os horários
  cores_hor = {
  '03:00': 'midnightblue',   # Madrugada - tom escuro para representar noite/madrugada
  '09:00': 'skyblue',         # Manhã - tom suave e claro, simbolizando o início do dia
  '15:00': 'orange',          # Tarde - tom quente, mais intenso
  '21:00': 'slategray'       # Noite - tom ainda quente, mas mais escuro para representar o final do dia
  }

  linestyles_hor = {
    '03:00': '-',         # Linha contínua para representar a tranquilidade e constância da madrugada
    '09:00': '--',        # Linha tracejada, representando o início da atividade do dia
    '15:00': '-.',        # Linha pontilhada e traçada, sugerindo a variação da tarde
    '21:00': ':'          # Linha pontilhada para simbolizar o cair da noite
  }

  # Criar o gráfico
  fig, ax = plt.subplots(figsize=(12, 6))

  # Lista para armazenar handles e labels para a legenda
  handles = []
  labels = []
  linestyle = '-'  # Default linestyle
  color = None  # Default color

  i = identificacao(pressao_lista, estacao_lista, ano_lista, horario_lista)

  lista_contagem = []

  #print(f'df_mestre: {df_mestre}')
  # Iterar sobre os DataFrames na coluna do DataFrame mestre
  for idx, df in enumerate(df_mestre['Dataframe_Probabilidade']):
    # Calcular a potência
    df['Potência'] = 0.5 * rho * A * (df['Velocidade_Vento_resultante_m/s'] ** 3) / 10**3  # Em kW
    # Calcular a potência ponderada
    df['Potência_Ponderada'] = df['Potência'] * df['Densidade_de_Probabilidade']

    df = df.sort_values(by='Velocidade_Vento_resultante_m/s')

    # Reatribuir o DataFrame modificado ao df_mestre
    df_mestre.at[idx, 'Dataframe_Probabilidade'] = df

    # Identificar a estação e o horário correspondentes
    estacao = df_mestre.loc[idx, 'Estação']
    horario = df_mestre.loc[idx, 'Horário']
    pressao = df_mestre.loc[idx, 'Pressão']
    ano = df_mestre.loc[idx, 'Ano']


    if i == [0, 0, 1, 1]:  # i = [i_pr, i_est, i_ano, i_hor]
      titulo = f'Potência Ponderada: Ano: {ano} - Horário: {horario}  (Diversas Pressões)'
      titulo_legenda = 'Estações'
      label = f'{estacao}'
      color = cores_est.get(estacao)
      variavel_contada = estacao


    elif i == [0, 1, 0, 1]:
      titulo = f'Potência Ponderada: Estação: {estacao} - Horário: {horario}  (Diversas Pressões)'
      titulo_legenda = 'Anos'
      label = f'{ano}'
      color = cores_hor.get(horario)
      variavel_contada = ano


    elif i == [0, 1, 1, 0]:
      titulo = f'Potência Ponderada: Estação: {estacao} - Ano: {ano}  (Diversas Pressões)'
      titulo_legenda = 'Horários'
      label = f'{horario}'
      color = cores_hor.get(horario)
      variavel_contada = horario


    elif i == [1, 0, 0, 1]:
      titulo = f'Potência Ponderada: Pressão: {pressao} - Horário: {horario}  (Diversos Anos)'
      titulo_legenda = 'Estações'
      label = f'{estacao}'
      color = cores_est.get(estacao)
      variavel_contada = estacao

    elif i == [1, 0, 1, 0]:
      titulo = f'Potência Ponderada: Pressão: {pressao} - Ano: {ano}  (Diversos Horários)'
      titulo_legenda = 'Estações'
      label = f'{estacao}'
      color = cores_est.get(estacao)
      variavel_contada = estacao

    elif i == [1, 1, 0, 0]:
      titulo = f'Potência Ponderada: Pressão: {pressao} - Estação: {estacao}  (Diversos Anos)'
      titulo_legenda = 'Horários'
      label = f'{horario}'
      color = cores_hor.get(horario)
      variavel_contada = horario

    elif i == [0, 1, 1, 1]:
      titulo = f'Potência Ponderada: Estação: {estacao} - Ano: {ano} - Horário: {horario}'
      titulo_legenda = 'Pressões'
      label = f'{pressao}'
      variavel_contada = pressao

    elif i == [1, 0, 1, 1]:
      titulo = f'Potência Ponderada: Pressão: {pressao} - Ano: {ano} - Horário: {horario}'
      titulo_legenda = 'Estações'
      label = f'{estacao}'
      color = cores_est.get(estacao)
      variavel_contada = estacao

    elif i == [1, 1, 0, 1]:
      titulo = f'Potência Ponderada: Pressão: {pressao} - Estação: {estacao} - Horário: {horario}'
      titulo_legenda = 'Ano'
      label = f'{ano}'
      variavel_contada = ano

    elif i == [1, 1, 1, 0]:
      titulo = f'Potência Ponderada: Pressão: {pressao} - Estação: {estacao} - Ano: {ano}'
      titulo_legenda = 'Horário'
      label = f'{horario}'
      color = cores_hor.get(horario)
      variavel_contada = horario

    elif i == [1, 1, 1, 1]:
      titulo = f'Potência Ponderada: Pressão: {pressao} - Estação: {estacao} - Ano: {ano} - Horário: {horario}'
      variavel_contada = None
      titulo_legenda = None

    line, = ax.plot(df['Velocidade_Vento_resultante_m/s'], df['Potência_Ponderada'], color = color, linestyle = linestyle)

    if variavel_contada not in lista_contagem and i != [1, 1, 1, 1]:  # Evita repetição na legenda
      lista_contagem.append(variavel_contada)
      handles.append(line)
      labels.append(label)

  #print(f'df: {df}')

  # Configurar o gráfico
  ax.set_title(titulo)
  ax.set_xlabel('Velocidade do Vento (m/s)')
  ax.set_ylabel('Potência Ponderada (kW/m^2)')
  ax.legend(handles=handles, labels=labels, title=titulo_legenda)  # Adiciona a legenda com os handles e labels armazenados)
  ax.grid(True)
  ax.minorticks_on()
  ax.grid(True, which='minor', alpha=0.3)

  # Exibir o gráfico
  plt.tight_layout()
  plt.show()

  return df_mestre
