from .usuario import valores_nao_aceitos


# Para facilitar a escolha da plataforma
def simplifica_plat(plataforma):

  valores_nao_aceitos(plataforma, ["1", "2", "3", "4", "5", "6", "7", "8", "9",
                                   'NAMORADO 2 (PNA-2)', 'PETROBRAS 26 (P-26)',
                                   'PETROBRAS 32 (P-32)', 'PETROBRAS 37 (P-37)',
                                   'PETROBRAS IX', 'PETROBRAS XIX', 'PETROBRAS XXXIII',
                                   'VERMELHO 1 (PVM-1)', 'VERMELHO 2 (PVM-2)'])
  
  if plataforma == '1':
    return 'NAMORADO 2 (PNA-2)'
  elif plataforma == '2':
    return 'PETROBRAS 26 (P-26)'
  elif plataforma == '3':
    return 'PETROBRAS 32 (P-32)'
  elif plataforma == '4':
    return 'PETROBRAS 37 (P-37)'
  elif plataforma == '5':
    return 'PETROBRAS IX'
  elif plataforma == '6':
    return 'PETROBRAS XIX'
  elif plataforma == '7':
    return 'PETROBRAS XXXIII'
  elif plataforma == '8':
    return 'VERMELHO 1 (PVM-1)'
  elif plataforma == '9':
    return 'VERMELHO 2 (PVM-2)'
  else:
    return plataforma
