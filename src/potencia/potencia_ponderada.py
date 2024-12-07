import pjenergy.main as mp
import src.outras.caso_zero as cz
import pandas as pd
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
  color = 'black'  # Default color

  i = identificacao(pressao_lista, estacao_lista, ano_lista, horario_lista)

  lista_contagem = []

  # Iterar sobre os DataFrames na coluna do DataFrame mestre
  for idx, df in enumerate(df_mestre['Dataframe_Probabilidade']):

    # Calcular a potência
    df['Potência'] = 0.5 * rho * A * (df['Velocidade_Vento_resultante_m/s'] ** 3) / 10**3  # Em kW
    # Calcular a potência ponderada
    df['Potência_Ponderada'] = df['Potência'] * df['Densidade_de_Probabilidade']

    df = df.sort_values(by='Velocidade_Vento_resultante_m/s')
    #print(df.head(40))
    #print('\n')
    #print(df.tail(40))

    # Identificar a estação e o horário correspondentes
    estacao = df_mestre.loc[idx, 'Estação']
    horario = df_mestre.loc[idx, 'Horário']
    pressao = df_mestre.loc[idx, 'Pressão']
    ano = df_mestre.loc[idx, 'Ano']


    if i == [0, 0, 1, 1]:  # i = [i_pr, i_est, i_ano, i_hor]
      titulo = f'Potência Ponderada: Ano {ano} - Horário: {horario}  (Diversas Pressões)'
      label = f'Est: {estacao}'
      color = cores_est.get(estacao)

      line, = ax.plot(df['Velocidade_Vento_resultante_m/s'], df['Potência_Ponderada'], color = color, linestyle = linestyle)

      if estacao not in lista_contagem:  # Evita repetição na legenda
        lista_contagem.append(estacao)
        handles.append(line)
        labels.append(label)
      print(f'lista_contagem: {lista_contagem}')
      print(f'handles: {handles}')
      print(f'labels: {labels}')

    elif i == [0, 1, 0, 1]:
      titulo = f'Potência Ponderada: Estação {estacao} - Horário: {horario}  (Diversas Pressões)'
      label = f'Ano: {ano}'
      color = None

      line, = ax.plot(df['Velocidade_Vento_resultante_m/s'], df['Potência_Ponderada'], color = color, linestyle = linestyle)

      if ano not in lista_contagem:  # Evita repetição na legenda
        lista_contagem.append(ano)
        handles.append(line)
        labels.append(label)

    elif i == [0, 1, 1, 0]:
      pass

    elif i == [1, 0, 0, 1]:
      pass

    elif i == [1, 0, 1, 0]:
      pass

    elif i == [1, 1, 0, 0]:
      pass

    elif i == [0, 1, 1, 1]:
      pass

    elif i == [1, 0, 1, 1]:
      pass

    elif i == [1, 1, 0, 1]:
      pass

    elif i == [1, 1, 1, 0]:
      pass

    elif i == [1, 1, 1, 1]:
      pass

    '''# Plotar a curva
    line, = ax.plot(df['Velocidade_Vento_resultante_m/s'], df['Potência_Ponderada'], color = color, linestyle = linestyle)
    if label not in labels:  # Evita duplicação na legenda
      handles.append(line)
      print(handles)
      labels.append(label)'''

  # Configurar o gráfico
  ax.set_title(titulo)
  ax.set_xlabel('Velocidade do Vento (m/s)')
  ax.set_ylabel('Potência Ponderada (kW/m^2)')
  ax.legend(handles=handles, labels=labels, title="Legenda")  # Adiciona a legenda com os handles e labels armazenados)
  ax.grid(True)
  ax.minorticks_on()
  ax.grid(True, which='minor', alpha=0.3)

  # Exibir o gráfico
  plt.tight_layout()
  plt.show()



def potencia(pressao, estacao, ano, horario):

  # Lista de caminhos para os arquivos CSV
  arquivos_csv = ['/content/pjenergy/data/dados_interpolados/df_interpolado_Verao.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Outono.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Inverno.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Primavera.csv']
  # Lista para armazenar os DataFrames
  dataframes = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
  # Concatenar todos os DataFrames em um único
  df_base = pd.concat(dataframes, ignore_index=True)

  variaveis_dict = {'Pressão': pressao, 'Estação': estacao, 'Ano': ano, 'Horário': horario}

  # Substituindo valores '0' usando cz.zero_para_todos
  for chave, valor in variaveis_dict.items():
    if valor == '0':
      variaveis_dict[chave] = cz.zero_para_todos(valor, chave)
  #print(estacao)
  df_mestre = pd.DataFrame(columns=['Pressão', 'Estação', 'Ano', 'Horário', 'Dataframe_Probabilidade'])

  df_base['Data'] = pd.to_datetime(df_base['Data'])
  df_base['Ano'] = df_base['Data'].dt.year

  contagem_todos = 0

  for chave, valor in variaveis_dict.items():
    #print(f'1 -> chave: {chave}, valor: {valor}')
    if valor in ['Todos', 'Todas']:
      #print(f'2 -> chave: {chave}, valor: {valor}')
      if chave == 'Pressão':
        pressao_lista = df_base['Nível_de_Pressão_hPa'].unique().tolist()
      elif chave == 'Estação':
        estacao_lista = df_base['Estação_do_Ano'].unique().tolist()
      elif chave == 'Ano':
        ano_lista = df_base['Ano'].unique().tolist()
      elif chave == 'Horário':
        horario_lista = df_base['Horário_Brasília'].unique().tolist()

      contagem_todos += 1

    else:
      #print(f'3 -> chave: {chave}, valor: {valor}')
      if chave == 'Pressão':
        pressao_lista = [float(valor)]
      elif chave == 'Estação':
        estacao_lista = [valor]
      elif chave == 'Ano':
        ano_lista = [int(valor)]
      elif chave == 'Horário':
        horario_lista = [valor]

  print(f'pressao_lista: {pressao_lista}')
  print(f'estacao_lista: {estacao_lista}')
  print(f'ano_lista: {ano_lista}')
  print(f'horario_lista: {horario_lista}')

  if contagem_todos > 2:
    return 'Variáveis demais com o valor "Todas" ou "0". Precisam ser no máximo duas.'

  for p in pressao_lista:
    for est in estacao_lista:
      #print(est)
      #print(estacao_lista)
      for an in ano_lista:
        for hor in horario_lista:
          df_prob_local = mp.prob(perguntas = False, pressao = p, estacao = est, ano = an, horario = hor, exibir_grafico=False)
          nova_linha = {'Pressão': p, 'Estação': est, 'Ano': an, 'Horário': hor, 'Dataframe_Probabilidade': df_prob_local}

          df_mestre = pd.concat([df_mestre, pd.DataFrame([nova_linha])], ignore_index=True)

  return df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista

def usuario_potencia(perguntas, pressao, estacao, ano, horario):

  '''Inicia a busca pelos argumentos do usuário'''

  if perguntas == True:
    pressao = input('Qual pressão deseja observar (em HPa)? Escolha um número inteiro entre 972 e 1000. Escreva Todas ou 0 para não filtrar nenhuma pressão específica. \n')
    estacao = input('Qual estação deseja observar? Escolha entre Verão, Outono, Inverno ou Primavera. Escreva Todas ou 0 para não filtrar nenhuma estação específica. \n')
    ano = input('Qual ano deseja observar? Escolha um número inteiro entre 2010 e 2023. Escreva Todos ou 0 para não filtrar nenhum ano específico. \n')
    horario = input('Qual horário deseja observar? Escolha entre 03:00, 09:00, 15:00 ou 21:00. Escreva Todos ou 0 para não filtrar nenhum horário específico. \n')

  else:
    pass

  try:
    df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista = potencia(pressao, estacao, ano, horario)
  except:
    print('Variáveis demais com o valor "Todas" ou "0". Precisam ser no máximo duas.')
    return

  pond_potencia(df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista)

  #return tabela