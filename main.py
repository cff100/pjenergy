import src.perfis.usuario as us
import src.perfis.numero_linhas_colunas as nlc
import src.perfis.iteracao_graficos as itg
import src.interpolacao.gera_tabela_interpolacao as gti
import matplotlib.pyplot as plt
import numpy as np

def main(perguntas = True, variavel = "Ambas", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Média", data = None, ano = "Todos"):

  dicionario_argumentos = us.argumentos_usuario(perguntas, variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)
  #print(dicionario_argumentos)

  if not isinstance(dicionario_argumentos, dict) or dicionario_argumentos['indicador'] == 'Sem_filtros':
    print('Não é possível criar um gráfico com essa combinação de data e estação \n Dataframe gerado:')
    return dicionario_argumentos

  n_lin, n_col = nlc.linhas_colunas(dicionario_argumentos)
  fig, axs = plt.subplots(n_lin, n_col, figsize=(9*n_col, 6*n_lin))

  # Garante que axs seja uma lista
  if isinstance(axs, np.ndarray):  # Se 'axs' for um array
    axs = axs.flatten().tolist()  # Converte para lista
  else:  # Se houver apenas um subplot (caso de 1x1)
    axs = [axs]  # Coloca o único subplot em uma lista

  #print(axs)

  itg.iteracao_grafico(dicionario_argumentos, axs)


  #return x

'''
def criacao_interpolacao(perguntas = True, variavel = "Ambas", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Média", data = None, ano = "Todos"):
  # Função que cria um dataframe com os valores interpolados (demora bastante de serconstruído)

  dicionario_argumentos = us.argumentos_usuario(perguntas, variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)

  if dicionario_argumentos['data'] == None and dicionario_argumentos['componente_velocidade'] in ['Resultante', None]:
    ti.interpolacao(dicionario_argumentos)
  else:
    if dicionario_argumentos['data'] != None:
      print('Quando uma data específica é escolhida, não é gerada uma tabela de interpolação')
    if dicionario_argumentos['componente_velocidade'] not in ['Resultante', None]:
      print('Não é gerada uma tabela de interpolação para tabelas de componentes específicas')
'''