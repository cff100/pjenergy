import src.perfis.usuario as us
import src.perfis.numero_linhas_colunas as nlc
import src.perfis.iteracao_graficos as itg
import src.distribuicao_probabilidade.dist_probabilidade as dp
import src.potencia.potencia_ponderada as pp
import src.potencia.potencia_comparacao_alturas as pca
import matplotlib.pyplot as plt
import numpy as np

def graf(perguntas = True, variavel = "Ambas", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Média", data = None, ano = "Todos", ling_graf = 'pt'):

  dicionario_argumentos = us.argumentos_usuario(perguntas, variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)

  if dicionario_argumentos == None:   # Ocorre quando há uma escolha errada de argumentos na escolha direta do usuário
    return
  elif dicionario_argumentos['indicador'] == 'Sem_filtros':
    print('Não é possível criar um gráfico com essa combinação de data e estação \n Dataframe gerado:')
    return dicionario_argumentos['df']


  n_lin, n_col = nlc.linhas_colunas(dicionario_argumentos)
  fig, axs = plt.subplots(n_lin, n_col, figsize=(9*n_col, 6*n_lin))

  # Garante que axs seja uma lista
  if isinstance(axs, np.ndarray):  # Se 'axs' for um array
    axs = axs.flatten().tolist()  # Converte para lista
  else:  # Se houver apenas um subplot (caso de 1x1)
    axs = [axs]  # Coloca o único subplot em uma lista

  itg.iteracao_grafico(dicionario_argumentos, axs, ling_graf)

def prob(perguntas = True, pressao = 'Todas', estacao = 'Todas', ano = 'Todos', horario = 'Todos', exibir_grafico=True):
  tabela_probabilidade = dp.usuario_weibull_velocidade(perguntas, pressao, estacao, ano, horario, exibir_grafico)
  return tabela_probabilidade

def pot(perguntas = True, pressao = 'Todas', estacao = 'Todas', ano = 'Todos', horario = 'Todos', plotar_graficos=True):
  df_mestre = pp.usuario_potencia(perguntas, pressao, estacao, ano, horario, plotar_graficos)
  return df_mestre

def pot_media(perguntas = True, l_vel_inf = 3, l_vel_sup = 24):
  plotar_graficos = False
  pca.potencia_altura(perguntas, l_vel_inf, l_vel_sup, plotar_graficos)
  #return
