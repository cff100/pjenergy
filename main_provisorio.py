import src.usuario as us

def main(perguntas = True, variavel = "Ambos", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Média", data = None, ano = "Todos"):
  dicionario_argumentos = us.argumentos_usuario(perguntas, variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)
  return dicionario_argumentos