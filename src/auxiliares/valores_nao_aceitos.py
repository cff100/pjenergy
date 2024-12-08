''' INFO
Verifica se o valor escolhido para o argumento está entre os válidos.
'''

def valores_nao_aceitos(valor_escolhido, valores_aceitos, dica = False, nome_variavel = None):

  '''Função que garante que a pergunta será repetida caso o usuário responda diferente das alternativas'''

  #print(dica)
  #print(f"Checando valor: {valor_escolhido}")
  if valor_escolhido not in valores_aceitos:
    if dica == True:
      print(f"ERRO: Valor não aceito para {nome_variavel}")
      print(f"Valores aceitos: {valores_aceitos} \n")
    else:
      print("ERRO: Valor não aceito")
      print('\n')
    return False
  else:
    #print(f"Valor escolhido: {valor_escolhido} \n")
    return valor_escolhido