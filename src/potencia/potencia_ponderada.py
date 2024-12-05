import pjenergy.main as mp
import src.outras.caso_zero as cz
import pandas as pd


def potencia(pressao, estacao, ano, horario):

  variaveis_dict = {'Pressão': pressao, 'Estação': estacao, 'Ano': ano, 'Horário': horario}

  # Substituindo valores '0' usando cz.zero_para_todos
  for chave, valor in variaveis_dict.items():
    if valor == '0':
      variaveis_dict[chave] = cz.zero_para_todos(valor, chave)

  df_mestre = pd.DataFrame(columns=['Pressão', 'Estação', 'Ano', 'Horário', 'Dataframe_Probabilidade'])

  variaveis_todos = []
  variaveis_especifico = []

  for chave, valor in variaveis_dict.items():
    if valor in ['Todos', 'Todas']:
      variaveis_todos.append(chave)
    else:
      variaveis_especifico.append(chave)

    # Realizando os loops para variáveis em 'variaveis_todos'
    for chave_todos in variaveis_todos:
      for chave_especifico in variaveis_especifico:
        # Aqui você pode executar sua lógica de combinação entre as variáveis
        print(f"Processando {chave_todos} com {chave_especifico}")


def usuario_potencia(perguntas, pressao, estacao, ano, horario):

  '''Inicia a busca pelos argumentos do usuário'''

  if perguntas == True:
    pressao = input('Qual pressão deseja observar (em HPa)? Escolha um número inteiro entre 972 e 1000. Escreva Todas ou 0 para não filtrar nenhuma pressão específica. \n')
    estacao = input('Qual estação deseja observar? Escolha entre Verão, Outono, Inverno ou Primavera. Escreva Todas ou 0 para não filtrar nenhuma estação específica. \n')
    ano = input('Qual ano deseja observar? Escolha um número inteiro entre 2010 e 2023. Escreva Todos ou 0 para não filtrar nenhum ano específico. \n')
    horario = input('Qual horário deseja observar? Escolha entre 03:00, 09:00, 15:00 ou 21:00. Escreva Todos ou 0 para não filtrar nenhum horário específico. \n')

  else:
    pass

  tabela = potencia(pressao, estacao, ano, horario)


  return tabela