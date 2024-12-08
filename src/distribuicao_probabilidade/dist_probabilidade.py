''' INFO
Gera um histograma e a distribuição de Weibull para a velocidade do vento,
além de uma tabela com os pontos dessa distribuição.
'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import weibull_min
import numpy as np
import warnings

horarios = ['03:00', '09:00', '15:00', '21:00']
plataforma_escolhida = "PETROBRAS XXXIII"

def plot_weibull_velocidade(pressao, estacao, ano, horario, exibir_grafico):

  # Lista de caminhos para os arquivos CSV
  arquivos_csv = ['/content/pjenergy/data/dados_interpolados/df_interpolado_Verao.csv',
                  '/content/pjenergy/data/dados_interpolados/df_interpolado_Outono.csv',
                  '/content/pjenergy/data/dados_interpolados/df_interpolado_Inverno.csv',
                  '/content/pjenergy/data/dados_interpolados/df_interpolado_Primavera.csv']
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
    
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore", category=UserWarning, message="Parsing .*")  # Exemplo para pandas
      df_combinado['Data'] = pd.to_datetime(df_combinado['Data'])
      #df_combinado.loc[:, 'Data'] = pd.to_datetime(df_combinado['Data'])
      df_combinado = df_combinado[df_combinado['Data'].dt.year == ano]

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
  df_combinado = df_combinado.sort_values(by='Velocidade_Vento_resultante_m/s')

  #print(df_combinado)

  velocidades = df_combinado['Velocidade_Vento_resultante_m/s'].copy()
  #velocidades.sort_values(inplace=True)

  # Ajustar a distribuição de Weibull
  params = weibull_min.fit(velocidades)
  weibull_pdf = weibull_min.pdf(velocidades, *params)

  df_combinado['Densidade_de_Probabilidade'] = weibull_pdf

  # Calcular a soma das probabilidades usando integração
  prob_sum = np.trapz(weibull_pdf, velocidades)  # Aproximação da integral

  #print(df_combinado)




  if exibir_grafico:

    # Verificar se a integral está próxima de 1
    if np.isclose(prob_sum, 1, atol=5e-2):
      print(f'A soma das probabilidades está correta (próxima de 1): {prob_sum}')
    else:
      print(f'⚠️ A soma das probabilidades não está próxima 1: {prob_sum}')


    # Criar a figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotar o histograma
    sns.histplot(velocidades, kde=False, stat='density', color='lightgray', alpha=0.5, bins=20, label='Dados')


    # Plotar a curva ajustada
    plt.plot(velocidades, weibull_pdf, label='Ajuste de Weibull', color='r', linewidth=2)

    ax.set_title(f'Histograma e Ajuste de Distribuição Weibull - Horário: {horario} - Pressão: {pressao} hPa - Estação: {estacao} - Ano: {ano}')
    texto = plataforma_escolhida
    ax.text(0.77, 0.85, f'Plataforma: {texto}', transform=ax.transAxes, fontsize=9, verticalalignment='top')

    # Configurações do gráfico
    plt.xlabel('Velocidade do Vento (m/s)', fontsize=14)
    plt.ylabel('Densidade de Probabilidade', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

  df_combinado = df_combinado.sort_values(by='Velocidade_Vento_resultante_m/s')
  #print(df_combinado.head(40))
  #print('\n')
  #print(df_combinado.tail(40))
  return df_combinado

def usuario_weibull_velocidade(perguntas, pressao, estacao, ano, horario, exibir_grafico):

  '''Inicia a busca pelos argumentos do usuário'''

  if perguntas == True:
    pressao = input('Qual pressão deseja observar (em HPa)? Escolha um número inteiro entre 972 e 1000. Escreva Todas ou 0 para não filtrar nenhuma pressão específica. \n')
    estacao = input('Qual estação deseja observar? Escolha entre Verão, Outono, Inverno ou Primavera. Escreva Todas ou 0 para não filtrar nenhuma estação específica. \n')
    ano = input('Qual ano deseja observar? Escolha um número inteiro entre 2010 e 2023. Escreva Todos ou 0 para não filtrar nenhum ano específico. \n')
    horario = input('Qual horário deseja observar? Escolha entre 03:00, 09:00, 15:00 ou 21:00. Escreva Todos ou 0 para não filtrar nenhum horário específico. \n')

  else:
    pass

  tabela = plot_weibull_velocidade(pressao, estacao, ano, horario, exibir_grafico)


  return tabela
