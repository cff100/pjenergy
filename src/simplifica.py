# Para facilitar a escolha da plataforma

def simplifica_funcao(plataforma):

  #print("Função ativada: simplifica_funcao \n")

  if plataforma == 'p1':
    return 'NAMORADO 2 (PNA-2)', None
  elif plataforma == 'p2':
    return 'PETROBRAS 26 (P-26)', None
  elif plataforma == 'p3':
    return 'PETROBRAS 32 (P-32)', None
  elif plataforma == 'p4':
    return 'PETROBRAS 37 (P-37)', None
  elif plataforma == 'p5':
    return 'PETROBRAS IX', None
  elif plataforma == 'p6':
    return 'PETROBRAS XIX', None
  elif plataforma == 'p7':
    return 'PETROBRAS XXXIII', None
  elif plataforma == 'p8':
    return 'VERMELHO 1 (PVM-1)', None
  elif plataforma == 'p9':
    return 'VERMELHO 2 (PVM-2)', None
  elif isinstance(plataforma, list):
    mensagem_erro = "Lista de plataformas não é aceito \n"
    return None, mensagem_erro
  else:
    return plataforma, None
