''' INFO
Função para traduzir variáveis de português para inglês para colocar nos gráficos.
'''

def trad_para_ingles(variavel):
  if variavel == 'Todos' or variavel == 'Todas':
    return 'All'
  elif variavel == 'Primavera':
    return 'Spring'
  elif variavel == 'Outono':
    return 'Summer'
  elif variavel == 'Inverno':
    return 'Winter'
  elif variavel == 'Outono':
    return 'Autumn'
  elif variavel == 'Resultante':
    return 'Resulting Vel.'
  else:
    return variavel
