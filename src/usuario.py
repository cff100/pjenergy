from .simplifica import simplifica_plat

def valores_nao_aceitos(valor_escolhido, valores_aceitos):
  if valor_escolhido not in valores_aceitos:
    print("Valor não aceito \n")
    return False
  else:
    return True



def perguntas_usuario():

  aceito_1, aceito_2, aceito_3, aceito_4, aceito_5, aceito_6, aceito_7 = [False] * 7


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

  while aceito_5 == False:
    indicador_dict = {
        '1': 'diario',
        '2': 'média'
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
    data = input(
      '''Qual dia deseja observar? Escreva no formato yyyy-mm-dd \n
      Exemplo: 2022-04-27 \n \n
    '''
    )

    print("\n")

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


  variavel = variaveis_dict[variavel]
  modo = modo_dict[modo]
  plataforma = plataformas_dict[plataforma]
  indicador = indicador_dict[indicador]


  argumentos = dict(
      variavel = variavel,
      modo = modo,
      componente = componente_velocidade,
      plataforma = plataforma,
      estacao = estacao,
      indicador = indicador,
      data = data

  )

  return argumentos

def escolha_direta_usuario(variavel, modo, componente_velocidade, plataforma, estacao, indicador, data):

  plataforma = simplifica_plat(plataforma)

  argumentos = dict(
        variavel = variavel,
        modo = modo,
        componente = componente_velocidade,
        plataforma = plataforma,
        estacao = estacao,
        indicador = indicador,
        data = data
    )
  
  return argumentos


def argumentos_usuario(perguntas = True, variavel = "Ambos", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Estações", data = None):
  if perguntas == True:
    argumentos = perguntas_usuario()
  else:
    argumentos = escolha_direta_usuario(variavel, modo, componente_velocidade, plataforma, estacao, indicador, data)
    

  return argumentos
  
