import src.auxiliares.valores_nao_aceitos as vna

def resp_usuario_2(perguntas, pressao, estacao, ano, horario):


  aceito_1, aceito_2, aceito_3, aceito_4 = [False] * 4

  # Para quando o usuário colocar os argumentos por meio das perguntas
  if perguntas == True:

    ''' --------------------------------
    Qual pressão a ser escolhida
    '''

    while aceito_1 == False:
      valores_aceitos = list(range(972,1001)) + ['0', 'Todas']
      valores_aceitos = [str(va) if va not in ('Todas', '0') else va for va in valores_aceitos]
      pressao = input('Qual pressão deseja observar (em HPa)? Escolha um número inteiro entre 972 e 1000. Escreva Todas ou 0 para não filtrar nenhuma pressão específica. \n')
      aceito_1 = vna.valores_nao_aceitos(pressao, valores_aceitos) # Verifica se é um valor aceito

      print('\n')


    ''' --------------------------------
    Qual estação a ser escolhida
    '''

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

      aceito_2 = vna.valores_nao_aceitos(estacao, ['0', '1', '2', '3', '4', 'Todas']) # Verifica se é um valor aceito
      if aceito_2 == True:
        if estacao != 'Todas':
          estacao = estacoes_dict[estacao]
      else:
        pass


    ''' --------------------------------
    Qual ano a ser escolhido
    '''

    while aceito_3 == False:
      valores_aceitos = list(range(2010,2024)) + ['0', 'Todos']
      valores_aceitos = [str(va) if va not in ('Todos', '0') else va for va in valores_aceitos]
      ano = input('Qual ano deseja observar? Escolha um número inteiro entre 2010 e 2023. Escreva Todos ou 0 para não filtrar nenhum ano específico. \n')
      aceito_3 = vna.valores_nao_aceitos(ano, valores_aceitos) # Verifica se é um valor aceito


    ''' --------------------------------
    Qual horário a ser escolhido
    '''
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


      aceito_4 = vna.valores_nao_aceitos(horario, ['0', '1', '2', '3', '4', 'Todos']) # Verifica se é um valor aceito
      if aceito_4 == True:
        if horario != 'Todos':
          horario = horario_dict[horario]
      else:
        pass





    # Print os argumentos escolhidos
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




  # Para quando o usuário colocar os argumentos diretamente
  else:
    # Converter pressão e ano para str
    if type(pressao) != str:
      pressao_str = str(int(pressao))
    else:
      pressao_str = pressao
    if type(ano) != str:
      ano_str = str(ano)
    else:
      ano_str = ano

    # Verificação da pressão
    valores_aceitos = list(range(972,1001)) + ['0', 'Todas']
    valores_aceitos = [str(va) if va not in ('Todas', '0') else va for va in valores_aceitos]
    aceito = vna.valores_nao_aceitos(pressao_str, valores_aceitos, dica = True, nome_variavel = 'pressão')
    if aceito == False:
      return None

    # Verificação da estação
    aceito = vna.valores_nao_aceitos(estacao, ['Verão', 'Outono', 'Inverno', 'Primavera', 'Todas', '0'], dica = True, nome_variavel = 'estação')
    if aceito == False:
      return None

    # Verificação do ano
    valores_aceitos = list(range(2010,2024)) + ['0', 'Todos']
    valores_aceitos = [str(va) if va not in ('Todos', '0') else va for va in valores_aceitos]
    aceito = vna.valores_nao_aceitos(ano_str, valores_aceitos, dica = True, nome_variavel = 'ano')
    if aceito == False:
      return None

    # Verificação do horário
    aceito = vna.valores_nao_aceitos(horario, ['03:00', '09:00', '15:00', '21:00', 'Todos', '0'], dica = True, nome_variavel = 'horário')
    if aceito == False:
      return None

  # Quando necessário, conversão de pressão para float e ano para int
  if pressao not in ['Todas', '0'] and type(pressao) != float:
    pressao = float(pressao)
  if ano not in ['Todos', '0'] and type(ano) != int:
    ano = int(ano)



  return pressao, estacao, ano, horario