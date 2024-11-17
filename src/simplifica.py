# Para facilitar a escolha da plataforma

def simplifica_funcao(plataforma):

  #print("Função ativada: simplifica_funcao \n")

  if plataforma == '1':
    return 'NAMORADO 2 (PNA-2)', None
  elif plataforma == '2':
    return 'PETROBRAS 26 (P-26)', None
  elif plataforma == '3':
    return 'PETROBRAS 32 (P-32)', None
  elif plataforma == '4':
    return 'PETROBRAS 37 (P-37)', None
  elif plataforma == '5':
    return 'PETROBRAS IX', None
  elif plataforma == '6':
    return 'PETROBRAS XIX', None
  elif plataforma == '7':
    return 'PETROBRAS XXXIII', None
  elif plataforma == '8':
    return 'VERMELHO 1 (PVM-1)', None
  elif plataforma == '9':
    return 'VERMELHO 2 (PVM-2)', None
  elif isinstance(plataforma, list):
    mensagem_erro = "Lista de plataformas não é aceito \n"
    return None, mensagem_erro
  else:
    return plataforma, None
