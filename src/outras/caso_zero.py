def zero_para_todos(variavel, nome_variavel):
  if nome_variavel in ['Estação', 'Pressão']:
    variavel = 'Todas'
  elif nome_variavel in ['Ano', 'Horário']:
    variavel = 'Todos'
  return variavel