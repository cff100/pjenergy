import src.usuario as us
import src.numero_linhas_colunas as nlc
import src.iteracao_graficos as itg
import matplotlib.pyplot as plt

def main(perguntas = True, variavel = "Ambas", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Média", data = None, ano = "Todos"):

  dicionario_argumentos = us.argumentos_usuario(perguntas, variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)

  if not isinstance(dicionario_argumentos, dict):
    print('Não é possível criar um gráfico com essa combinação de data e estação \n Dataframe gerado:')
    return dicionario_argumentos

  n_lin, n_col = nlc.linhas_colunas(dicionario_argumentos)
  fig, axs = plt.subplots(n_lin, n_col, figsize=(9*n_col, 6*n_lin))
  
  x = itg.iteracao_grafico(dicionario_argumentos)



  return x #axs, (n_lin, n_col), fig, dicionario_argumentos
