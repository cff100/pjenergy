import pandas as pd
from datetime import datetime
from .simplifica import simplifica_plat
from .valores_nao_aceitos import valores_nao_aceitos


def dataframe_plataforma_escolhida(plataforma):
  df = pd.read_csv(f'/content/pjenergy/data/dataframes_ventos_por_plataforma/Era5_Vento_CAMPOS-{plataforma}.csv', index_col=0)
  return df


def formato_data(data_escolhida, dica = False):

  '''Verifica se a data escolhida está no formato aceito'''

  if data_escolhida == None:
    return True
  try:
    datetime.strptime(data_escolhida, '%Y-%m-%d')
    return True
  except ValueError:
    print("ERRO: Formato de data inválido \n")
    if dica == True:
      print("Formato aceito: yyyy-mm-dd \n")
    return False



def presenca_data(data_escolhida, df):

  '''Verifica se a data escolhida está presente no dataframe'''

  if (df['Data'] == data_escolhida).any() or data_escolhida == None:
    return True
  else:
    print(f"ERRO: A string '{data_escolhida}' não está presente no dataframe. \n")
    return False


def verifica_ano(ano, df, dica = False, nome_variavel = None):

  '''Verifica se o ano escolhido está presente no dataframe ou se não há escolha específica para ano'''

  if ano == '0' or ano == 'Todos':
    ano = 'Todos'
    aceito_8 = True
  else:
    # Cria uma lista dos anos existentes no dataframe
    anos_dataframe = pd.to_datetime(df['Data']).dt.year.unique()
    anos_dataframe = [str(a) for a in anos_dataframe]
    # Ordena os anos
    anos_dataframe.sort()
    # Verifica se é um valor aceito
    aceito_8 = valores_nao_aceitos(ano, anos_dataframe, dica, nome_variavel)
  return aceito_8, ano


def perguntas_usuario():

  '''
  Faz perguntas ao usuário sobre os argumentos importantes para a formação dos gráficos.
  Esse é um dos modos de obter os argumentos. É o modo mais longo.
  '''

  #Variável que determina se a pergunta deve ser repetida
  aceito_1, aceito_2, aceito_3, aceito_4, aceito_5, aceito_6, aceito_7, aceito_8, aceito_9 = [False] * 9


  while aceito_1 == False:
    variaveis_dict = {
        "1": "Velocidade",
        "2": "Temperatura",
        "3": "Ambos"
    }

    variavel = input(
        '''Qual variável deseja observar? \n
        1 - Velocidade \n
        2 - Temperatura \n
        3 - Ambos \n \n'''
        )

    print("\n")

    aceito_1 = valores_nao_aceitos(variavel, ["1", "2", "3"])




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

    aceito_2 = valores_nao_aceitos(modo, ["1", "2"])


  if variavel in ['1','3']:

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

      aceito_3 = valores_nao_aceitos(componente_velocidade, ["1", "2", "3"])
      componente_velocidade = componente_velocidade_dict[componente_velocidade]

  else:
    componente_velocidade = None


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

    aceito_4 = valores_nao_aceitos(plataforma, ["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    plataforma = plataformas_dict[plataforma]
    df = dataframe_plataforma_escolhida(plataforma)
    df.drop(columns=['Plataforma'], inplace = True)

  while aceito_5 == False:
    indicador_dict = {
        '1': 'Diário',
        '2': 'Média'
    }

    indicador = input(
        '''Deseja observar um dia específico ou estações do ano? \n
        1 - Dia \n
        2 - Estações \n \n'''
    )

    print("\n")

    aceito_5 = valores_nao_aceitos(indicador, ['1', '2'])

  if indicador == "1":
    estacao = None
    ano = 'Todos'
    while aceito_9 == False:
      data = input(
        '''Qual dia deseja observar? Escreva no formato yyyy-mm-dd \n
        Exemplo: 2022-04-27 \n \n
      '''
      )

      print("\n")

      aceito_9 = formato_data(data)
      if aceito_9 == True:
        aceito_9 = presenca_data(data, df)
      if data != None:
        df = df[df['Data'] == data]
        df.drop(columns=['Data'], inplace = True)




  elif indicador == "2":
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
          6 - Geral (juntas) \n \n'''

      )

      print("\n")

      aceito_7 = valores_nao_aceitos(estacao, ['1', '2', '3', '4', '5'])

      estacao = estacoes_dict[estacao]

      if estacao in ['Verão', 'Outono', 'Inverno', 'Primavera']:
        df = df[df['Estação_do_Ano'] == estacao]
        df.drop(columns=['Estação_do_Ano'], inplace = True)

      # Escolha do ano
      while aceito_8 == False:
        ano = input(
            '''Qual ano deseja observar? (Digite 0 caso queira incluir todos os anos) \n \n
            '''
        )

        print("\n")

        aceito_8, ano = verifica_ano(ano, df)
        if ano not in ['0', 'Todos']:
          df['Ano'] = df['Data'].str[:4]
          df = df[df['Ano'] == ano]
          df.drop(columns=['Ano'], inplace = True)




  variavel = variaveis_dict[variavel]
  modo = modo_dict[modo]
  indicador = indicador_dict[indicador]


  argumentos = dict(
      variavel = variavel,
      modo = modo,
      componente = componente_velocidade,
      plataforma = plataforma,
      estacao = estacao,
      indicador = indicador,
      data = data,
      ano = ano,
      df = df
  )

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
    estacao = 'Geral'

  aceito_ano, ano = verifica_ano(ano, df, dica = True, nome_variavel = 'ano')
  if aceito_ano == False:
    return None

  if ano not in ['0', 'Todos']:
    df['Ano'] = df['Data'].str[:4]
    df = df[df['Ano'] == ano]
    df.drop(columns=['Ano'], inplace = True)



  aceito_data = formato_data(data)
  if aceito_data == True:
    aceito_data = presenca_data(data, df)
  if aceito_data == False:
    return None

  if data != None:
    df = df[df['Data'] == data]
    df.drop(columns=['Data'], inplace = True)


  variavel = valores_nao_aceitos(variavel, ["Velocidade", "Temperatura", "Ambos"], dica = True, nome_variavel = 'variavel')
  if variavel == False:
    return None

  modo = valores_nao_aceitos(modo, ["Original", "Original-Derivada"], dica = True, nome_variavel = 'modo')
  if modo == False:
    return None

  componente_velocidade = valores_nao_aceitos(componente_velocidade, ["Resultante", "u", "v"], dica = True, nome_variavel = 'componente_velocidade')
  if componente_velocidade == False:
    return None

  estacao = valores_nao_aceitos(estacao, ["Verão", "Outono", "Inverno", "Primavera", "Todas", "Geral"], dica = True, nome_variavel = 'estacao')
  if estacao == False:
    return None

  if estacao in ['Verão', 'Outono', 'Inverno', 'Primavera']:
    df = df[df['Estação_do_Ano'] == estacao]
    df.drop(columns=['Estação_do_Ano'], inplace = True)

  indicador = valores_nao_aceitos(indicador, ["Diário", "Média"], dica = True, nome_variavel = 'indicador')
  if indicador == False:
    return None

  argumentos = dict(
        variavel = variavel,
        modo = modo,
        componente = componente_velocidade,
        plataforma = plataforma,
        estacao = estacao,
        indicador = indicador,
        data = data,
        ano = ano,
        df = df
    )

  return argumentos


def argumentos_usuario(perguntas = True, variavel = "Ambos", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Média", data = None, ano = "Todos"):

  '''Inicia a busca pelos argumentos do usuário'''

  if perguntas == True:
    argumentos = perguntas_usuario()
  else:
    argumentos = escolha_direta_usuario(variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)


  return argumentos
