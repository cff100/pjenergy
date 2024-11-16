def valores_nao_aceitos(valor_escolhido, valores_aceitos):
  if valor_escolhido not in valores_aceitos:
    print("Valor não aceito \n")
    return False
  else:
    return True


def perguntas_usuario():
  aceito_1 = False
  aceito_2 = False
  aceito_3 = False
  aceito_4 = False

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
    

  if variavel in ['1', '2']:

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
      

    if variavel == '1':

      while aceito_3 == False:
        componente_dict = {
            "1": "Resultante",
            "2": "u",
            "3": "v"
        }

        componente = input(
          '''Qual componente deseja observar? \n 
          1 - Resultante \n 
          2 - u \n 
          3 - v \n \n'''
        )

        print("\n")

        aceito_3 = valores_nao_aceitos(componente, ["1", "2", "3"])

  while aceito_4 == False:
    plataformas_dict = {
        "p1": 'NAMORADO 2 (PNA-2)',
        "p2": 'PETROBRAS 26 (P-26)',
        "p3": 'PETROBRAS 32 (P-32)',
        "p4": 'PETROBRAS 37 (P-37)',
        "p5": 'PETROBRAS IX',
        "p6": 'PETROBRAS XIX',
        "p7": 'PETROBRAS XXXIII',
        "p8": 'VERMELHO 1 (PVM-1)',
        "p9": 'VERMELHO 2 (PVM-2)'

    }
    plataforma = input(
      '''Qual plataforma deseja observar? \n
      p1 - NAMORADO 2 (PNA-2) \n
      p2 - PETROBRAS 26 (P-26) \n
      p3 - PETROBRAS 32 (P-32) \n
      p4 - PETROBRAS 37 (P-37) \n
      p5 - PETROBRAS IX \n
      p6 - PETROBRAS XIX \n
      p7 - PETROBRAS XXXIII \n
      p8 - VERMELHO 1 (PVM-1) \n
      p9 - VERMELHO 2 (PVM-2) \n \n'''
    )

    print("\n")

    aceito_4 = valores_nao_aceitos(plataforma, ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9"])



  variavel = variaveis_dict[variavel]
  modo = modo_dict[modo]
  componente = componente_dict[componente]
  plataforma = plataformas_dict[plataforma]

  argumentos = dict(
      variavel = variavel,
      modo = modo,
      componente = componente,
      plataforma = plataforma
  )

  return argumentos

