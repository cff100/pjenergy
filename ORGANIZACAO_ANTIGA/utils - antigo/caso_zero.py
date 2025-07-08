''' INFO
Como alternativa a "Todos" ou "Todas", o uso do "0" com valor válido para as variáveis tem como objetivo apenas 
facilitar o uso das funções pelo usuário no caso em que ele queira usar 
todos os valores disponíveis para aquele argumento.

Para se obter um nome significativo, a função abaixo converte o valor da variavel igual a "0" para "Todos" ou "Todas".
'''

def zero_para_todos(variavel, nome_variavel):
  if nome_variavel in ['Estação', 'Pressão']:
    variavel = 'Todas'
  elif nome_variavel in ['Ano', 'Horário']:
    variavel = 'Todos'
  return variavel