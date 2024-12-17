''' INFO
Recebe o input do usuário, filtra e cria o dataframe que será utilizado para a plotagem dos gráficos.
'''


import pjenergy.main as mp
import src.auxiliares.caso_zero as cz
import src.auxiliares.respostas_usuario as ru
import pandas as pd
from .grafico_potencia_ponderada import pond_potencia
import traceback


def potencia(pressao, estacao, ano, horario, plotar_graficos):

  '''Cria o dataframe que será usado para gerar o gráfico'''

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

  # Obtém e trata os argumentos de entrada do usuário
  pressao, estacao, ano, horario = ru.resp_usuario_2(perguntas, pressao, estacao, ano, horario)

  # Cria o dataframe que será usado para gerar o gráfico
  df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista = potencia(pressao, estacao, ano, horario, plotar_graficos)

  
  if pressao_lista is None:
    return df_mestre

  # Geração do gráfico de potência ponderada
  df_mestre = pond_potencia(df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista, plotar_graficos)

  return df_mestre
