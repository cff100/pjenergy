''' INFO
Calcula a potência pondera e cria um gráfico para ela.
'''


import matplotlib.pyplot as plt
import src.utils.traduzir_para_ingles as ti
import src.utils.pressao_para_altura as pa

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







def pond_potencia(df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista, plotar_graficos, ling_graf):

  ''' Para criar o gráfico da potência ponderada'''

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



  # Lista para armazenar handles e labels para a legenda
  handles = []
  labels = []
  linestyle = '-'  # Default linestyle
  color = None  # Default color
  ax_criado = False

  i = identificacao(pressao_lista, estacao_lista, ano_lista, horario_lista)

  lista_contagem = []

  # Para deixar o gráfico mais limpo, diminuir o número de pressões consideradas no caso em que diversas pressões são plotadas
  if i == [0, 1, 1, 1]:
    pressao_manter = [pressao_par for pressao_par in pressao_lista if pressao_par % 2 == 0]  
    df_mestre = df_mestre[df_mestre['Pressão'].isin(pressao_manter)]
    df_mestre = df_mestre.reset_index(drop=True)


  # Iterar sobre os DataFrames na coluna do DataFrame mestre
  for idx, df in enumerate(df_mestre['Dataframe_Probabilidade']):
    # Calcular a potência
    df['Potência'] = 0.5 * rho * A * (df['Velocidade_Vento_resultante_m/s'] ** 3) / 10**3  # Em kW
    # Calcular a potência ponderada
    df['Potência_Ponderada'] = df['Potência'] * df['Densidade_de_Probabilidade']

    df = df.sort_values(by='Velocidade_Vento_resultante_m/s')

    # Reatribuir o DataFrame modificado ao df_mestre
    df_mestre.at[idx, 'Dataframe_Probabilidade'] = df

    if plotar_graficos == False:
      return df_mestre

    # Identificar a estação e o horário correspondentes
    estacao = df_mestre.loc[idx, 'Estação']
    horario = df_mestre.loc[idx, 'Horário']
    pressao = df_mestre.loc[idx, 'Pressão']
    ano = df_mestre.loc[idx, 'Ano']

    # Converter o nome das variáveis para inglês quando necessário
    if ling_graf == 'pt':
      pass
    elif ling_graf == 'en':
      pressao = ti.trad_para_ingles(pressao)
      estacao = ti.trad_para_ingles(estacao)
      horario = ti.trad_para_ingles(horario)
      ano = ti.trad_para_ingles(ano)

    #if contagem_grafico == 0:
    if ax_criado == False:
      # Criar o gráfico
      fig, ax = plt.subplots(figsize=(12, 6))
      ax_criado = True


    if i == [0, 0, 1, 1]:  # i = [i_pr, i_est, i_ano, i_hor]
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Ano: {ano} - Horário: {horario}  (Diversas Pressões)'
        titulo_legenda = 'Estações'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Year: {ano} - Hour: {horario}  (Various Pressures)'
        titulo_legenda = 'Seasons'
      label = f'{estacao}'
      color = cores_est.get(estacao)
      variavel_contada = estacao


    elif i == [0, 1, 0, 1]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Estação: {estacao} - Horário: {horario}  (Diversas Pressões)'
        titulo_legenda = 'Anos'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Season: {estacao} - Hour: {horario}  (Various Pressures)'
        titulo_legenda = 'Years'
      label = f'{ano}'
      variavel_contada = ano


    elif i == [0, 1, 1, 0]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Estação: {estacao} - Ano: {ano}  (Diversas Pressões)'
        titulo_legenda = 'Horários'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Season: {estacao} - Year: {ano}  (Various Pressures)'
        titulo_legenda = 'Hours'
      label = f'{horario}'
      color = cores_hor.get(horario)
      variavel_contada = horario


    elif i == [1, 0, 0, 1]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Pressão: {pressao} - Horário: {horario}  (Diversos Anos)'
        titulo_legenda = 'Estações'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Pressure: {pressao} - Hour: {horario}  (Various Years)'
        titulo_legenda = 'Seasons'
      label = f'{estacao}'
      color = cores_est.get(estacao)
      variavel_contada = estacao

    elif i == [1, 0, 1, 0]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Pressão: {pressao} - Ano: {ano}  (Diversos Horários)'
        titulo_legenda = 'Estações'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Pressure: {pressao} - Year: {ano}  (Various Hours)'
        titulo_legenda = 'Seasons'
      label = f'{estacao}'
      color = cores_est.get(estacao)
      variavel_contada = estacao

    elif i == [1, 1, 0, 0]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Pressão: {pressao} - Estação: {estacao}  (Diversos Anos)'
        titulo_legenda = 'Horários'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Pressure: {pressao} - Season: {estacao}  (Various Years)'
        titulo_legenda = 'Hours'
      label = f'{horario}'
      color = cores_hor.get(horario)
      variavel_contada = horario

    elif i == [0, 1, 1, 1]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Estação: {estacao} - Ano: {ano} - Horário: {horario}'
        titulo_legenda = 'Pressões'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Season: {estacao} - Year: {ano} - Hour: {horario}'
        titulo_legenda = 'Pressures'
      altura = int(pa.pressao_para_altura(pressao/10)) # Cálculo da altura correspondente àquela pressão
      label = f'{pressao} ({altura} m)'
      variavel_contada = pressao

    elif i == [1, 0, 1, 1]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Pressão: {pressao} - Ano: {ano} - Horário: {horario}'
        titulo_legenda = 'Estações'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Pressure: {pressao} - Year: {ano} - Hour: {horario}'
        titulo_legenda = 'Seasons'
      label = f'{estacao}'
      color = cores_est.get(estacao)
      variavel_contada = estacao

    elif i == [1, 1, 0, 1]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Pressão: {pressao} - Estação: {estacao} - Horário: {horario}'
        titulo_legenda = 'Ano'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Pressure: {pressao} - Season: {estacao} - Hour: {horario}'
        titulo_legenda = 'Year'
      label = f'{ano}'
      variavel_contada = ano

    elif i == [1, 1, 1, 0]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Pressão: {pressao} - Estação: {estacao} - Ano: {ano}'
        titulo_legenda = 'Horário'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Pressure: {pressao} - Season: {estacao} - Year: {ano}'
        titulo_legenda = 'Hour'
      label = f'{horario}'
      color = cores_hor.get(horario)
      variavel_contada = horario

    elif i == [1, 1, 1, 1]:
      if ling_graf == 'pt':
        titulo = f'Potência Ponderada: Pressão: {pressao} - Estação: {estacao} - Ano: {ano} - Horário: {horario}'
      elif ling_graf == 'en':
        titulo = f'Weighted Power: Pressure: {pressao} - Season: {estacao} - Year: {ano} - Hour: {horario}'
      variavel_contada = None
      titulo_legenda = None

    line, = ax.plot(df['Velocidade_Vento_resultante_m/s'], df['Potência_Ponderada'], color = color, linestyle = linestyle)

    if variavel_contada not in lista_contagem and i != [1, 1, 1, 1]:  # Evita repetição na legenda
      lista_contagem.append(variavel_contada)
      handles.append(line)
      labels.append(label)


  # Configurar o gráfico
  ax.set_title(titulo)
  if ling_graf == 'pt':
    ax.set_xlabel('Velocidade do Vento (m/s)')
    ax.set_ylabel('Potência Ponderada (kW/m^2)')
  elif ling_graf == 'en':
    ax.set_xlabel('Wind Speed (m/s)')
    ax.set_ylabel('Weighted Power (kW/m^2)')
  ax.legend(handles=handles, labels=labels, title=titulo_legenda)  # Adiciona a legenda com os handles e labels armazenados)
  ax.grid(True)
  ax.minorticks_on()
  ax.grid(True, which='minor', alpha=0.3)

  # Exibir o gráfico
  plt.tight_layout()
  plt.show()

  return df_mestre
