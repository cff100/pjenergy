''' INFO
Gera os gráficos de perfil de velocidade e tempertura.
'''


import matplotlib.pyplot as plt
import numpy as np

def criacao_grafico(ax, cor, Y, X, Y_smooth, X_smooth, grafico, plataforma, estacao, horario, variavel, componente_velocidade, data):

  horarios = ['03:00', '09:00', '15:00', '21:00']

  # Verifica o tipo de gráfico a ser gerado
  if grafico == 'original':

    # Gera um gráfico de dispersão para os dados originais
    ax.scatter(X, Y, color=cor)
    # Plota uma linha suavizada usando os valores interpolados de X e Y
    ax.plot(X_smooth, Y_smooth, color=cor, label=f'Horário {horario}', linestyle='-')

    # Configuração do título e do eixo X de acordo com o tipo de dado (velocidade ou temperatura)
    if variavel == 'velocidade':
      if data == None:
        ax.set_title(f'Perfil de Velocidade do Vento - {plataforma} - Est: {estacao} - Dir: {componente_velocidade}')  # Define o título para perfis de velocidade
      else:
        ax.set_title(f'Perfil de Velocidade do Vento - {plataforma} - Est: {estacao} - Data: {data} - Dir: {componente_velocidade}')  # Define o título para perfis de velocidade
      ax.set_xlabel('Velocidade do Vento (m/s)')  # Nome do eixo X para velocidade
    elif variavel == 'temperatura':
      if data == None:
        ax.set_title(f'Perfil de Temperatura - {plataforma} - Est: {estacao}')  # Define o título para perfis de temperatura
      else:
        ax.set_title(f'Perfil de Temperatura - {plataforma} - Est: {estacao} - Data: {data}')  # Define o título para perfis de temperatura
      ax.set_xlabel('Temperatura (°C)') # Nome do eixo X para temperatura

  elif grafico == 'derivada':

    # Calcula a derivada dos dados suavizados (gradiente da variável X em relação a Y)
    derivada_X_smooth = np.gradient(X_smooth, Y_smooth)
    # Plota a derivada dos dados
    ax.plot(derivada_X_smooth, Y_smooth, color=cor, label=f'Horário {horario}', linestyle='--')

    # Adiciona uma linha vertical em x=0 depois do último horário (ex: 21:00)
    if horario == horarios[-1]:
      ax.axvline(x=0, color='black', linestyle='-', alpha=0.5, label='x = 0')  # Cria a linha vertical

    # Configuração do título e do eixo X de acordo com o tipo de dado (derivada de velocidade ou de temperatura)
    if variavel == 'velocidade':
      if data == None:
        ax.set_title(f'Derivada do Perfil de Velocidade - {plataforma} - Est: {estacao}) - - Dir: {componente_velocidade}')  # Título para derivada de velocidade
      else:
        ax.set_title(f'Derivada do Perfil de Velocidade - {plataforma} - Est: {estacao} - Data: {data} - - Dir: {componente_velocidade}')  # Título para derivada de velocidade

      ax.set_xlabel('Derivada da Velocidade do Vento')  # Nome do eixo X para derivada de velocidade
    elif variavel == 'temperatura':
      if data == None:
        ax.set_title(f'Derivada do Perfil de Temperatura - {plataforma} - Est: {estacao}')  # Título para derivada de temperatura
      else:
        ax.set_title(f'Derivada do Perfil de Temperatura - {plataforma} - Est: {estacao} - Data: {data}')  # Título para derivada de temperatura

      ax.set_xlabel('Derivada da Temperatura') # Nome do eixo X para derivada de temperatura

  # Configurações comuns para os eixos dos gráficos (independente do tipo de dado)
  ax.set_ylabel('Altitude (m)') # Nome do eixo Y
  ax.grid(True)  # Adiciona uma grade ao gráfico
  ax.grid(True, which='both') # Habilita tanto a grade principal quanto a secundária
  ax.minorticks_on() # Ativa as marcas menores nos eixos
  ax.grid(which='minor', linestyle=':', linewidth=0.5) # Configura o estilo da grade menor (linhas pontilhadas e mais finas)
  ax.legend() # Adiciona uma legenda ao gráfico
