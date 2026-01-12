''' INFO
Calcula a altura a partir do valor da pressão atmosférica.
'''

import math

def pressao_para_altura(P_h):

  PA = 101.325  # Pressão atmosférica ao nível do mar em kPa
  k = 1.21e-5   # Constante em s²/m²
  g = 9.81      # Aceleração gravitacional em m/s²

  # P_h: Pressão a uma altura h (em KPa)
  altura = -math.log(P_h / PA) / (k * g)
  return altura