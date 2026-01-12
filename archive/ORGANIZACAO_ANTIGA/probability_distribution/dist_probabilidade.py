

''' INFO
Gera um histograma e a distribuição de Weibull para a velocidade do vento,
além de uma tabela com os pontos dessa distribuição.
'''

import src.utils.traduzir_para_ingles as ti
import src.utils.respostas_usuario as ru
from ast import arguments
#from scipy.integrate import simps
import scipy.integrate
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import weibull_min
import numpy as np
import warnings

horarios = ['03:00', '09:00', '15:00', '21:00']
plataforma_escolhida = "PETROBRAS XXXIII"

def plot_weibull_velocidade(pressao, estacao, ano, horario, exibir_grafico, ling_graf):

  # Lista de caminhos para os arquivos CSV
  arquivos_csv = ['/content/pjenergy/data/dados_interpolados/df_interpolado_Verao.csv',
                  '/content/pjenergy/data/dados_interpolados/df_interpolado_Outono.csv',
                  '/content/pjenergy/data/dados_interpolados/df_interpolado_Inverno.csv',
                  '/content/pjenergy/data/dados_interpolados/df_interpolado_Primavera.csv']

  # Lista para armazenar os DataFrames
  dataframes = [pd.read_csv(arquivo) for arquivo in arquivos_csv]

  # Concatenar todos os DataFrames em um único
  df_combinado = pd.concat(dataframes, ignore_index=True)
  #print(df_combinado)

  # Filtrar pressão
  if pressao not in ['Todas', '0']:
    df_combinado = df_combinado[df_combinado['Nível_de_Pressão_hPa'] == float(pressao)]
  else:
    if pressao == '0':
      pressao = 'Todas'

  # Filtrar estação
  if estacao not in ['Todas', '0']:
    df_combinado = df_combinado[df_combinado['Estação_do_Ano'] == estacao]
  else:
    if estacao == '0':
      estacao = 'Todas'

  # Filtrar ano
  if ano not in ['Todos', '0']:

    df_combinado['Data'] = pd.to_datetime(df_combinado['Data'])
    #df_combinado.loc[:, 'Data'] = pd.to_datetime(df_combinado['Data'])
    df_combinado = df_combinado[df_combinado['Data'].dt.year == ano]
  else:
    if ano == '0':
      ano = 'Todos'

  # Filtrar horário
  if horario not in ['Todos', '0']:
    df_combinado = df_combinado[df_combinado['Horário_Brasília'] == horario]
  else:
    if horario == '0':
      horario = 'Todos'


  # Resetar o índice após todos os filtros
  df_combinado.reset_index(drop=True, inplace=True)
  df_combinado = df_combinado.sort_values(by='Velocidade_Vento_resultante_m/s')


  # Extrair a coluna de velocidades do vento
  velocidades = df_combinado['Velocidade_Vento_resultante_m/s'].copy()
  #print(velocidades)

  # Ajustar a distribuição de Weibull
  params = weibull_min.fit(velocidades)
  weibull_pdf = weibull_min.pdf(velocidades, *params)

  # Criar uma coluna de densidades de probabilidade
  df_combinado['Densidade_de_Probabilidade'] = weibull_pdf

  # Calcular a soma das probabilidades usando integração
  #prob_sum = simps(weibull_pdf, velocidades)  # Aproximação da integral
  prob_sum = scipy.integrate.simps(weibull_pdf, velocidades)  # Aproximação da integral


  if exibir_grafico:

    # Verificar se a integral está próxima de 1
    if np.isclose(prob_sum, 1, atol=0.02):
      print(f'A soma das probabilidades está correta (próxima de 1): {prob_sum}')
    else:
      print(f'⚠️ A soma das probabilidades não está próxima 1: {prob_sum}')


    # Criar a figura
    fig, ax = plt.subplots(figsize=(10, 6))

    if ling_graf == 'pt':
      label_1 = 'Dados'
      label_2 = 'Ajuste de Weibull'
    elif ling_graf == 'en':
      label_1 = 'Data'
      label_2 = 'Weibull Fit'
      pressao = ti.trad_para_ingles(pressao)
      estacao = ti.trad_para_ingles(estacao)
      horario = ti.trad_para_ingles(horario)
      ano = ti.trad_para_ingles(ano)


    
    # Plotar o histograma
    sns.histplot(velocidades, kde=False, stat='density', color='lightgray', alpha=0.5, bins=20, label=label_1)


    # Plotar a curva ajustada
    plt.plot(velocidades, weibull_pdf, label=label_2, color='r', linewidth=2)

    if ling_graf == 'pt':
      ax.set_title(f'Histograma e Ajuste de Distribuição Weibull - Horário: {horario} - Pressão: {pressao} (hPa) - Estação: {estacao} - Ano: {ano}')
    elif ling_graf == 'en':
      ax.set_title(f'Histogram and Weibull Distribution Fit - Time: {horario} - Pressure: {pressao} (hPa) - Season: {estacao} - Year: {ano}')
    texto = plataforma_escolhida
    if ling_graf == 'pt':
      ax.text(0.77, 0.85, f'Plataforma: {texto}', transform=ax.transAxes, fontsize=9, verticalalignment='top')
    elif ling_graf == 'en':
      ax.text(0.77, 0.85, f'Platform: {texto}', transform=ax.transAxes, fontsize=9, verticalalignment='top')

    # Configurações do gráfico
    if ling_graf == 'pt':
      plt.xlabel('Velocidade do Vento (m/s)', fontsize=14)
      plt.ylabel('Densidade de Probabilidade', fontsize=14)
    elif ling_graf == 'en':
      plt.xlabel('Wind Speed (m/s)', fontsize=14)
      plt.ylabel('Probability Density', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

  df_combinado = df_combinado.sort_values(by='Velocidade_Vento_resultante_m/s')
  return df_combinado






def usuario_weibull_velocidade(perguntas, pressao, estacao, ano, horario, exibir_grafico, ling_graf):

  '''Inicia a busca pelos argumentos do usuário'''

  # Obtém e trata os argumentos de entrada do usuário
  pressao, estacao, ano, horario = ru.resp_usuario_2(perguntas, pressao, estacao, ano, horario)

  # Chama a função que cria o dataframe com os valores da densidade de probabilidade
  tabela = plot_weibull_velocidade(pressao, estacao, ano, horario, exibir_grafico, ling_graf)
  tabela.reset_index(drop=True, inplace=True)

  return tabela
