import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import weibull_min
import numpy as np

horarios = ['03:00', '09:00', '15:00', '21:00']
plataforma_escolhida = "PETROBRAS XXXIII"

def plot_weibull_velocidade(pressao, estacao, ano, horario):


  # Lista de caminhos para os arquivos CSV
  arquivos_csv = ['/content/pjenergy/data/dados_interpolados/df_interpolado_Verao.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Outono.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Inverno.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Primavera.csv']

  # Lista para armazenar os DataFrames
  dataframes = [pd.read_csv(arquivo) for arquivo in arquivos_csv]

  # Concatenar todos os DataFrames em um único
  df_combinado = pd.concat(dataframes, ignore_index=True)

  if pressao not in ['Todas', '0']:
    df_combinado = df_combinado[df_combinado['Nível_de_Pressão_hPa'] == float(pressao)]
  else:
    if pressao == '0':
      pressao = 'Todas'

  if estacao not in ['Todas', '0']:
    df_combinado = df_combinado[df_combinado['Estação_do_Ano'] == estacao]
  else:
    if estacao == '0':
      estacao = 'Todas'

  if ano not in ['Todos', '0']:
    df_combinado['Data'] = pd.to_datetime(df_combinado['Data'])
    df_combinado = df_combinado[df_combinado['Data'].dt.year == int(ano)]
  else:
    if ano == '0':
      ano = 'Todos'
  
  if horario not in ['Todos', '0']:
    df_combinado = df_combinado[df_combinado['Horário_Brasília'] == horario]
  else:
    if horario == '0':
      horario = 'Todos'

  # Resetar o índice após todos os filtros
  df_combinado.reset_index(drop=True, inplace=True)

  #print(df_combinado)

  velocidades = df_combinado['Velocidade_Vento_resultante_m/s'].copy()
  velocidades.sort_values(inplace=True)

  # Criar a figura
  plt.figure(figsize=(10, 6))

  # Plotar o histograma
  sns.histplot(velocidades, kde=False, stat='density', color='lightgray', alpha=0.5, bins=20, label='Dados')

  # Ajustar a distribuição de Weibull
  params = weibull_min.fit(velocidades)
  #x = np.linspace(min(df_velocidade), max(df_velocidade), 100)
  weibull_pdf = weibull_min.pdf(velocidades, *params)

  #df_combinado['x'] = velocidades
  df_combinado['Densidade_de_Probabilidade'] = weibull_pdf

  # Calcular a soma das probabilidades usando integração
  prob_sum = np.trapz(weibull_pdf, velocidades)  # Aproximação da integral
  #print(f'A soma aproximada da probabilidade (integral): {prob_sum}')

  print(df_combinado)

  # Plotar a curva ajustada
  plt.plot(velocidades, weibull_pdf, label='Ajuste de Weibull', color='r', linewidth=2)

  # Configurações do gráfico
  plt.xlabel('Velocidade do Vento (m/s)', fontsize=14)
  plt.ylabel('Densidade de Probabilidade', fontsize=14)
  plt.title('Histograma e Ajuste de Weibull', fontsize=16)
  plt.legend(fontsize=12)
  plt.grid(axis='y', linestyle='--', alpha=0.7)
  plt.show()

  # Verificar se a integral está próxima de 1
  if np.isclose(prob_sum, 1, atol=5e-2):
    print(f'A soma das probabilidades está correta: {prob_sum}')
  else:
    print(f'⚠️ A soma das probabilidades não está próxima 1: {prob_sum}')


  '''
    if pressao or estacao:
      if not estacao:
        ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Pressão: {pressao} hPa - Ano: {ano}')
      elif not pressao:
        ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Estação: {estacao} - Ano: {ano}')
      else:
        ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Pressão: {pressao} hPa - Estação: {estacao} - Ano: {ano}')
    else:
      ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Ano: {ano}')


    texto = plataforma_escolhida
    ax.text(0.73, 0.95, f'Plataforma: {texto}', transform=ax.transAxes, fontsize=9, verticalalignment='top')

  # Ajustar espaçamento entre os subplots
  plt.tight_layout()
  plt.show()

  print('\n')

  # Exibir a tabela de probabilidades
  #print(tabela_probabilidades)
  # Verificar se a soma da densidade de probabilidade está próxima de 1 para cada horário
  for horario in horarios:
    prob_sum = tabela_probabilidades[tabela_probabilidades['Horário'] == horario]['Densidade de Probabilidade'].sum()
    if np.isclose(prob_sum, 1, atol=1e-6):  # atol define a margem de erro aceitável
        print(f'A soma das probabilidades para o horário {horario} está correta: {prob_sum}')
    else:
        print(f'⚠️ A soma das probabilidades para o horário {horario} não é 1: {prob_sum}')


  # Salvar a tabela em um arquivo CSV, se desejado
  tabela_probabilidades.to_csv(f'Velocidade_Tabela_Probabilidades_Weibull.csv', index=False)

  return tabela_probabilidades'''


def usuario_weibull_velocidade(perguntas, pressao, estacao, ano, horario):

  '''Inicia a busca pelos argumentos do usuário'''

  if perguntas == True:
    pressao = input('Qual pressão deseja observar (em HPa)? Escolha um número inteiro entre 972 e 1000. Escreva Todas ou 0 para não filtrar nenhuma pressão específica. \n')
    estacao = input('Qual estação deseja observar? Escolha entre Verão, Outono, Inverno ou Primavera. Escreva Todas ou 0 para não filtrar nenhuma estação específica. \n')
    ano = input('Qual ano deseja observar? Escolha um número inteiro entre 2010 e 2023. Escreva Todos ou 0 para não filtrar nenhum ano específico. \n')
    horario = input('Qual horário deseja observar? Escolha entre 03:00, 09:00, 15:00 ou 21:00. Escreva Todos ou 0 para não filtrar nenhum horário específico. \n')

  else:
    pass

  tabela = plot_weibull_velocidade(pressao, estacao, ano, horario)


  return tabela
