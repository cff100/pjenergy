''' INFO
Recebe o input do usuário e o usa para filtrar e calcular médias do banco de dados, quando necessário.
'''


import pandas as pd
from datetime import datetime
from .simplifica import simplifica_plat
import src.auxiliares.valores_nao_aceitos as vna
from .dataframe_media import dataframe_media
from IPython.core.debugger import set_trace
#set_trace()

def dataframe_plataforma_escolhida(plataforma):
  df = pd.read_csv(f'/content/pjenergy/data/dataframe_ventos/dataframes_ventos_por_plataforma/Era5_Vento_CAMPOS-{plataforma}.csv', index_col=0)
  return df

def formato_data(data_escolhida, dica = False):

  '''Verifica se a data escolhida está no formato aceito'''

  try:
    datetime.strptime(data_escolhida, '%Y-%m-%d')
    return True     # Caso a string da data escolhida aceite a mudança de formato
  except ValueError:
    print("ERRO: Formato de data inválido \n")
    if dica == True:     # Para quando é necessário reforçar qual o formato aceito
      print("Formato aceito: yyyy-mm-dd \n")
    return False



def presenca_data(data_escolhida, df):

  '''Caso seja escolhida uma data, verifica se a data escolhida está presente no dataframe'''

  if (df['Data'] == data_escolhida).any():
    return True
  else:
    print(f"ERRO: A string '{data_escolhida}' não está presente no dataframe. \n")
    return False


def verifica_ano(ano, df, dica = False, nome_variavel = None):

  '''Verifica se o ano escolhido está presente no dataframe ou se não há escolha específica para ano'''


  ano_inteiro = int(ano)
  # Cria uma lista dos anos existentes no dataframe
  anos_dataframe = pd.to_datetime(df['Data']).dt.year.unique()
  anos_dataframe = [a for a in anos_dataframe]
  # Ordena os anos
  anos_dataframe.sort()
  # Verifica se é um valor aceito
  aceito_8 = vna.valores_nao_aceitos(ano_inteiro, anos_dataframe, dica, nome_variavel)

  return aceito_8


def print_argumentos(argumentos):
  # Lista de chaves para o primeiro dicionário
  keys_dict2 = ['df']
  keys_dict3 = ['df_para_interpolacao']

  # Separar os dicionários
  dict1 = {k: v for k, v in argumentos.items() if k not in keys_dict2 + keys_dict3}
  dict2 = {k: v for k, v in argumentos.items() if k in keys_dict2}
  dict3 = {k: v for k, v in argumentos.items() if k in keys_dict3}

  print(dict1)
  print('\n \n')
  #print(dict2)
  print('\n \n')
  #print(dict3)



def perguntas_usuario():

  '''
  Faz perguntas ao usuário sobre os argumentos importantes para a formação dos gráficos.
  Esse é um dos modos de obter os argumentos. É o modo mais longo.
  '''

  #Variável que determina se a pergunta deve ser repetida
  aceito_1, aceito_2, aceito_3, aceito_4, aceito_5, aceito_6, aceito_7, aceito_8, aceito_9 = [False] * 9


  # Qual variavel a ser escolhida
  while aceito_1 == False:
    # Dicionário que indica o nome de cada opção
    variaveis_dict = {
        "1": "Velocidade",
        "2": "Temperatura",
        "3": "Ambas"
    }

    # Pergunta para o usuário
    variavel = input(
        '''Qual variável deseja observar? \n
        1 - Velocidade \n
        2 - Temperatura \n
        3 - Ambas \n \n'''
        )

    print("\n")

    aceito_1 = vna.valores_nao_aceitos(variavel, ["1", "2", "3"]) # Verifica se é um valor aceito

    if aceito_1 == True:
      variavel = variaveis_dict[variavel]




  # Qual o modo a ser escolhido
  while aceito_2 == False:
    modo_dict = {
        "1": "Original",
        "2": "Original-Derivada"
    }

    modo = input(
      '''Qual modo deseja observar? \n
      1 - Original \n
      2 - Original-Derivada \n \n'''
    )

    print("\n")

    aceito_2 = vna.valores_nao_aceitos(modo, ["1", "2"])

    if aceito_2 == True:
      modo = modo_dict[modo]


  if variavel in ["Velocidade", "Ambas"]: # Caso a variável escolhida inclua velocidade

    if variavel == "Ambas" and modo == 'Original-Derivada':
      print("Devido à escolha de ambas variáveis:")
      modo = 'Original'
      print(f"- Modo foi alterado para {modo} \n")

    while aceito_3 == False:
      componente_velocidade_dict = {
          "1": "Resultante",
          "2": "u",
          "3": "v"
      }

      componente_velocidade = input(
        '''Qual componente da velocidade deseja observar? \n
        1 - Resultante \n
        2 - u \n
        3 - v \n \n'''
      )

      print("\n")

      aceito_3 = vna.valores_nao_aceitos(componente_velocidade, ["1", "2", "3"])

      if aceito_3 == True:
        componente_velocidade = componente_velocidade_dict[componente_velocidade] # Recebe o nome real da opção escolhida

  else:
    componente_velocidade = None   # Caso a variável escolhida seja apenas temperatura





  while aceito_4 == False:
    plataformas_dict = {
        "1": 'NAMORADO 2 (PNA-2)',
        "2": 'PETROBRAS 26 (P-26)',
        "3": 'PETROBRAS 32 (P-32)',
        "4": 'PETROBRAS 37 (P-37)',
        "5": 'PETROBRAS IX',
        "6": 'PETROBRAS XIX',
        "7": 'PETROBRAS XXXIII',
        "8": 'VERMELHO 1 (PVM-1)',
        "9": 'VERMELHO 2 (PVM-2)'

    }
    plataforma = input(
      '''Qual plataforma deseja observar? \n
      1 - NAMORADO 2 (PNA-2) \n
      2 - PETROBRAS 26 (P-26) \n
      3 - PETROBRAS 32 (P-32) \n
      4 - PETROBRAS 37 (P-37) \n
      5 - PETROBRAS IX \n
      6 - PETROBRAS XIX \n
      7 - PETROBRAS XXXIII \n
      8 - VERMELHO 1 (PVM-1) \n
      9 - VERMELHO 2 (PVM-2) \n \n'''
    )

    print("\n")

    aceito_4 = vna.valores_nao_aceitos(plataforma, ["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    if aceito_4 == True:
      plataforma = plataformas_dict[plataforma]
      df = dataframe_plataforma_escolhida(plataforma)  # Para escolher o arquivo csv específico da plataforma escolhida
      df.drop(columns=['Plataforma'], inplace = True)  # Exclui a coluna de plataformas




  while aceito_5 == False:
    indicador_dict = {
        '1': 'Diário',
        '2': 'Média',
        '3': 'Sem_filtros'
    }

    indicador = input(
        '''Deseja observar um dia específico ou estações do ano? Ou não deseja colocar filtros? \n
        1 - Dia \n
        2 - Estações \n
        3 - Sem filtros \n \n'''
    )

    print("\n")

    aceito_5 = vna.valores_nao_aceitos(indicador, ['1', '2', '3'])

    if aceito_5 == True:
      indicador = indicador_dict[indicador]

  if indicador == 'Sem_filtros':
    # Escolha automática de outros argumentos
    estacao = None
    ano = 'Todos'
    data = None
    df_para_interpolacao = df.copy()

  elif indicador == 'Diário':  # Se o indicador é Diário, é pedido para escolher um dia
    # Escolha automática de outros argumentos
    estacao = None
    ano = 'Todos' # Para que o ano correspondente a data não seja deixado de fora


    while aceito_9 == False:
      data = input(
        '''Qual dia deseja observar? Escreva no formato yyyy-mm-dd \n
        Exemplo: 2022-04-27 \n \n
      '''
      )

      print("\n")

      if data != None:
        aceito_9 = formato_data(data)  # Verificação do formato da data
        if aceito_9 == True:
          aceito_9 = presenca_data(data, df) # Verificação da presença da data no dataframe
          df = df[df['Data'] == data]  # Filtra os dataframe para a data escolhida
          df.drop(columns=['Data'], inplace = True)
      else:
        aceito_9 = True


    df_para_interpolacao = df.copy() #?




  elif indicador == 'Média': # Se o indicador é Média, é perguntado sobre a escolha de estação
    # Escolha automática de outros argumentos
    data = None

    while aceito_7 == False:
      estacoes_dict = {
        '1': 'Verão',
        '2': 'Outono',
        '3': 'Inverno',
        '4': 'Primavera',
        '5': 'Todas',
        '6': 'Geral'
      }

      estacao = input(
          '''Qual estação deseja observar? \n
          1 - Verão \n
          2 - Outono \n
          3 - Inverno \n
          4 - Primavera \n
          5 - Todas (separadas) \n
          6 - Geral (juntas) \n \n''' # Mantém as datas do dataframe

      )

      print("\n")

      aceito_7 = vna.valores_nao_aceitos(estacao, ['1', '2', '3', '4', '5', '6'])

      if aceito_7 == False:
        continue

      estacao = estacoes_dict[estacao]

      # Filtra os dataframe para a estação escolhida
      if estacao in ['Verão', 'Outono', 'Inverno', 'Primavera']:
        df = df[df['Estação_do_Ano'] == estacao]
        df.drop(columns=['Estação_do_Ano'], inplace = True)

      # Para garantir um número limite de subplots gerados, escolher todas estações pode causar modificações em outros argumentos.
      elif estacao == 'Todas':
        if modo == 'Original-Derivada' or variavel == 'Ambas':
          print("Devido à escolha das estações como 'Todas':")
          if modo == 'Original-Derivada':
            modo = 'Original'
            print(f"- Modo foi alterado para {modo} \n")
          if variavel == 'Ambas':
            variavel = 'Velocidade'
            print(f"- Variável precisa ser 'Velocidade' ou 'Temperatura'. Variável foi alterada automaticamente para {variavel} \n")



      # Qual ano deve ser escolhido
      while aceito_8 == False:
        ano = input(
            '''Qual ano deseja observar? (Digite 0 caso queira incluir todos os anos) \n \n
            '''
        )

        print("\n")

        if ano in ['0', 'Todos']:
          ano = 'Todos'
          aceito_8 = True
        else: # if ano not in ['0', 'Todos']:
          aceito_8 = verifica_ano(ano, df)

          if aceito_8 == False:
            continue

          # Filtra os dataframe para o ano escolhido
            df['Ano'] = df['Data'].str[:4]
            df = df[df['Ano'] == ano]
            df.drop(columns=['Ano'], inplace = True)

      df_para_interpolacao = df.copy()
      if estacao == None: # Sempre vai ocorrer quando uma data específica for escolhida ou simplesmente quando o usuário não escolher filtrar estação
        pass
      else:   # Chama a função que faz a média
        if estacao == 'Todas':
          estacoes_separadas = True  # Define que a média será para cada estação
        else:
          estacoes_separadas = False
        df = dataframe_media(df, estacoes_separadas)



  # Dipõe os argomentos em um dicionário
  argumentos = dict(
      variavel = variavel,
      modo = modo,
      componente_velocidade = componente_velocidade,
      plataforma = plataforma,
      estacao = estacao,
      indicador = indicador,
      data = data,
      ano = ano,
      df = df,
      df_para_interpolacao = df_para_interpolacao
  )

  print_argumentos(argumentos)

  return argumentos




def escolha_direta_usuario(variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano):

  '''
  O usuário coloca os argumentos de forma direta.
  Esse é o outro modo de obter os argumentos.
  '''

  # Chama uma função que converte o número representativo no nome da plataforma, além de verificar se não foi escolhida uma string invalida.
  #O nome completo da plataforma também é uma entrada válida.
  plataforma = simplifica_plat(plataforma)
  if plataforma == False:
    return None

  # Escolhe o dataframe da plataforma escolhida
  df = dataframe_plataforma_escolhida(plataforma)
  df.drop(columns=['Plataforma'], inplace = True)

  # Para alterar argumentos a partir da escolha do argumento prioritário data.
  if data != None:
    ano = '0'
    indicador = 'Diário'
    estacao = None
    if estacao != None or ano != '0' and indicador != 'Diário':
      print("Devido a escolha de uma data específica:")
      if estacao != None:
        estacao = None
        print(f'- Estação foi alterada para {estacao} \n')
      if ano != 'Todos':
        ano = 'Todos'
        print(f'- Ano foi alterado para {ano} \n')
      if indicador != 'Diário':
        indicador = 'Diário'
        print(f'- Indicador foi alterado para {indicador} \n')


  # Verifica a validade do ano e filtra o dataframe
  aceito_ano, ano = verifica_ano(ano, df, dica = True, nome_variavel = 'ano')
  if aceito_ano == False:
    return None
  if ano not in ['0', 'Todos']:
    df['Ano'] = df['Data'].str[:4]
    df = df[df['Ano'] == ano]
    df.drop(columns=['Ano'], inplace = True)

  # Verifica o formato, a presença da data e filtra o dataframe
  if data != None:
    aceito_data = formato_data(data)
    if aceito_data == True:
      aceito_data = presenca_data(data, df)
    if aceito_data == False:
      return None
    df = df[df['Data'] == data]
    df.drop(columns=['Data'], inplace = True)
    df = df.reset_index(drop = True)

  aceito = vna.valores_nao_aceitos(variavel, ["Velocidade", "Temperatura", "Ambas"], dica = True, nome_variavel = 'variavel')
  if aceito == False:
    return None
  elif variavel == "Temperatura":
    componente_velocidade = None

  aceito = vna.valores_nao_aceitos(modo, ["Original", "Original-Derivada"], dica = True, nome_variavel = 'modo')
  if aceito == False:
    return None
  elif variavel == "Ambas" and modo == 'Original-Derivada':
    print("Devido à escolha de ambas variáveis:")
    modo = 'Original'
    print(f"- Modo foi alterado para {modo} \n")

  aceito = vna.valores_nao_aceitos(componente_velocidade, ["Resultante", "u", "v", None], dica = True, nome_variavel = 'componente_velocidade')
  if aceito == False:
    return None

  aceito = vna.valores_nao_aceitos(estacao, ["Verão", "Outono", "Inverno", "Primavera", "Todas", "Geral", None], dica = True, nome_variavel = 'estacao')
  if aceito == False:
    return None
  elif estacao in ['Verão', 'Outono', 'Inverno', 'Primavera', 'Geral']:
    if estacao != 'Geral':
      df = df[df['Estação_do_Ano'] == estacao]
    #df.drop(columns=['Estação_do_Ano'], inplace = True)
  elif estacao == 'Todas': # Para garantir um número limite de subplots gerados, escolher todas estações pode causar modificações em outros argumentos.
    if modo != 'Original' or variavel == 'Ambas':
      print("Devido à escolha das estações como 'Todas':")
      if modo != 'Original':
        modo = 'Original'
        print(f"- Modo foi alterado para {modo} \n")
      if variavel == 'Ambas':
        variavel = 'Velocidade'
        print(f"- Variável precisa ser 'Velocidade' ou 'Temperatura'. Variável foi alterada automaticamente para {variavel} \n")
  else:
    if data == None and indicador != 'Sem_filtros':
      print("Devido à escolha de data e estacao como None:")
      indicador = 'Sem_filtros'
      print(f"- Indicador foi alterado para {indicador} \n")
      return df




  aceito = vna.valores_nao_aceitos(indicador, ["Diário", "Média", 'Sem_filtros'], dica = True, nome_variavel = 'indicador')
  if aceito == False:
    return None

  df_para_interpolacao = df.copy()

  # Verificar se é necessário fazer uma média e chamar a função que o faz
  if estacao == None: # Sempre vai ocorrer quando uma data específica for escolhida ou simplesmente quando o usuário não escolher filtrar estação
    pass
  else:
    if estacao == 'Todas':
      estacoes_separadas = True
    else:
      estacoes_separadas = False
    df = dataframe_media(df, estacoes_separadas)


  argumentos = dict(
        variavel = variavel,
        modo = modo,
        componente_velocidade = componente_velocidade,
        plataforma = plataforma,
        estacao = estacao,
        indicador = indicador,
        data = data,
        ano = ano,
        df = df,
        df_para_interpolacao = df_para_interpolacao
    )

  print_argumentos(argumentos)
  #print(argumentos)
  return argumentos


# Quando estacao e data são None ao mesmo tempo, o dataframe não seria processado o suficiente para plotagem, mas ainda serve para visualização da tabela
def argumentos_usuario(perguntas, variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano):

  '''Inicia a busca pelos argumentos do usuário'''

  if perguntas == True:
    argumentos = perguntas_usuario()
  else:
    argumentos = escolha_direta_usuario(variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)


  return argumentos
