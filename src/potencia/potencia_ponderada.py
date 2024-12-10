''' INFO
Recebe o input do usuário, filtra e cria o dataframe que será utilizado para a plotagem dos gráficos.
'''


import pjenergy.main as mp
import src.auxiliares.caso_zero as cz
import src.auxiliares.valores_nao_aceitos as vna
import pandas as pd
from .grafico_potencia_ponderada import pond_potencia
import traceback


def potencia(pressao, estacao, ano, horario, plotar_graficos):

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

  if plotar_graficos == True:
    print(f'pressao_lista: {pressao_lista}')
    print(f'estacao_lista: {estacao_lista}')
    print(f'ano_lista: {ano_lista}')
    print(f'horario_lista: {horario_lista}')

  if contagem_todos > 2:
    print(f'contagem_todos: {contagem_todos}')
    return 'Variáveis demais com o valor "Todas" ou "0". Precisam ser no máximo duas.', None, None, None, None

  # Inicializar o DataFrame corretamente
  df_mestre = pd.DataFrame(columns=['Pressão', 'Estação', 'Ano', 'Horário', 'Dataframe_Probabilidade'])

  for p in pressao_lista:
    for est in estacao_lista:
      for an in ano_lista:
        for hor in horario_lista:
          # Gerar o DataFrame local
          df_prob_local = mp.prob(perguntas=False, pressao=p, estacao=est, ano=an, horario=hor, exibir_grafico=False)

          # Verificar se é válido antes de adicionar
          if df_prob_local is not None:
            nova_linha = {
                'Pressão': p,
                'Estação': est,
                'Ano': an,
                'Horário': hor,
                'Dataframe_Probabilidade': df_prob_local
            }



            # Concatenar a nova linha
            df_mestre = pd.concat([df_mestre, pd.DataFrame([nova_linha])], ignore_index=True)



  return df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista












def usuario_potencia(perguntas, pressao, estacao, ano, horario, plotar_graficos):

  '''Inicia a busca pelos argumentos do usuário'''

  aceito_1, aceito_2, aceito_3, aceito_4 = [False] * 4

  if perguntas == True:
    while aceito_1 == False:
      valores_aceitos = list(range(972,1001)) + ['0', 'Todas']
      valores_aceitos = [str(va) if va not in ('Todas', '0') else va for va in valores_aceitos]
      pressao = input('Qual pressão deseja observar (em HPa)? Escolha um número inteiro entre 972 e 1000. Escreva Todas ou 0 para não filtrar nenhuma pressão específica. \n')
      aceito_1 = vna.valores_nao_aceitos(pressao, valores_aceitos) # Verifica se é um valor aceito

      print('\n')

    while aceito_2 == False:
      estacoes_dict = {
        '0': 'Todas',
        '1': 'Verão',
        '2': 'Outono',
        '3': 'Inverno',
        '4': 'Primavera',
      }

      estacao = input(
          '''Qual estação deseja observar? \n
          0 - Todas \n
          1 - Verão \n
          2 - Outono \n
          3 - Inverno \n
          4 - Primavera \n \n'''
          )

      print("\n")
      #estacao = input('Qual estação deseja observar? Escolha entre Verão, Outono, Inverno ou Primavera. Escreva Todas ou 0 para não filtrar nenhuma estação específica. \n')
      #estacao = estacoes_dict[estacao]
      aceito_2 = vna.valores_nao_aceitos(estacao, ['0', '1', '2', '3', '4', 'Todas']) # Verifica se é um valor aceito
      if aceito_2 == True:
        if estacao != 'Todas':
          estacao = estacoes_dict[estacao]
        #print(estacao)
      else:
        pass
      #aceito_2 = vna.valores_nao_aceitos(estacao, ['Verão', 'Outono', 'Inverno', 'Primavera', '0', 'Todas']) # Verifica se é um valor aceito

    while aceito_3 == False:
      valores_aceitos = list(range(2010,2024)) + ['0', 'Todos']
      valores_aceitos = [str(va) if va not in ('Todos', '0') else va for va in valores_aceitos]
      ano = input('Qual ano deseja observar? Escolha um número inteiro entre 2010 e 2023. Escreva Todos ou 0 para não filtrar nenhum ano específico. \n')
      aceito_3 = vna.valores_nao_aceitos(ano, valores_aceitos) # Verifica se é um valor aceito

    while aceito_4 == False:
      horario_dict = {
        '0': 'Todos',
        '1': '03:00',
        '2': '09:00',
        '3': '15:00',
        '4': '21:00',
      }

      horario = input(
          '''Qual horário deseja observar? \n
          0 - Todos \n
          1 - 03:00 \n
          2 - 09:00 \n
          3 - 15:00 \n
          4 - 21:00 \n \n'''
          )

      print("\n")

      #horario = input('Qual horário deseja observar? Escolha entre 03:00, 09:00, 15:00 ou 21:00. Escreva Todos ou 0 para não filtrar nenhum horário específico. \n')
      aceito_4 = vna.valores_nao_aceitos(horario, ['0', '1', '2', '3', '4', 'Todos']) # Verifica se é um valor aceito
      if aceito_4 == True:
        if horario != 'Todos':
          horario = horario_dict[horario]
      else:
        pass

    if pressao == '0':
      print('Pressão: Todas')
    else:
      print(f'Pressão: {pressao} hPa')
    print(f'Estação: {estacao}')
    if ano == '0':
      print('Ano: Todos')
    else:
      print(f'Ano: {ano}')
    print(f'Horário: {horario}')

  else:

    if type(pressao) != str:
      pressao = str(int(pressao))
    if type(ano) != str:
      ano = str(ano)
      
    valores_aceitos = list(range(972,1001)) + ['0', 'Todas']
    valores_aceitos = [str(va) if va not in ('Todas', '0') else va for va in valores_aceitos]
    aceito = vna.valores_nao_aceitos(pressao, valores_aceitos, dica = True, nome_variavel = 'pressão')
    if aceito == False:
      return None

    aceito = vna.valores_nao_aceitos(estacao, ['Verão', 'Outono', 'Inverno', 'Primavera', 'Todas', '0'], dica = True, nome_variavel = 'estação')
    if aceito == False:
      return None

    valores_aceitos = list(range(2010,2024)) + ['0', 'Todos']
    valores_aceitos = [str(va) if va not in ('Todos', '0') else va for va in valores_aceitos]
    aceito = vna.valores_nao_aceitos(str(ano), valores_aceitos, dica = True, nome_variavel = 'ano')
    if aceito == False:
      return None

    aceito = vna.valores_nao_aceitos(horario, ['03:00', '09:00', '15:00', '21:00', 'Todos', '0'], dica = True, nome_variavel = 'horário')
    if aceito == False:
      return None

  try:
    pressao = float(pressao)
  except:
    pass

  '''try:
    ano = int(ano)
  except:
    pass
  '''
  


  df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista = potencia(pressao, estacao, ano, horario, plotar_graficos)
  
  df_mestre = pond_potencia(df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista, plotar_graficos)

  return df_mestre
