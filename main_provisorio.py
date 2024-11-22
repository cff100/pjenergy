import src.usuario as us

def main_provisorio(perguntas = True, variavel = "Ambos", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Média", data = None, ano = "Todos"):
  a = us.argumentos_usuario(perguntas, variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)
  return a['variavel']