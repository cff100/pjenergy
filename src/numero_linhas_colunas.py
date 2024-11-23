def linhas_colunas(dicionario_argumentos):

  variavel = dicionario_argumentos['variavel']
  modo = dicionario_argumentos['modo']
  estacao = dicionario_argumentos['estacao']
  indicador = dicionario_argumentos['indicador']
  data = dicionario_argumentos['data']

  if variavel in ["Velocidade", "Temperatura"]:
    if modo == "Original":
      if indicador == 'Média':
        if estacao in ["Verão", "Outono", "Inverno", "Primavera", "Geral"]:
          n_lin, n_col = 1,1
        else: 
          n_lin, n_col = 2,2
      elif indicador == 'Diário':
        n_lin, n_col = 1,1
    elif modo == "Original-Derivada":
      if indicador == 'Média':
        n_lin, n_col = 1,2
      elif indicador == 'Diário':
        n_lin, n_col = 1,2

  elif variavel == "Ambas"
    if indicador == 'Média':
      n_lin, n_col = 1,2
    elif indicador == 'Diário':
      n_lin, n_col = 1,2
        


  return n_lin, n_col

