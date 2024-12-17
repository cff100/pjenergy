''' INFO
Gera os gráficos de perfil de velocidade e tempertura.
'''

import src.auxiliares.traduzir_para_ingles as ti
import matplotlib.pyplot as plt
import numpy as np

def criacao_grafico(ax, cor, Y, X, Y_smooth, X_smooth, grafico, plataforma, estacao, horario, variavel, componente_velocidade, data, ano, ling_graf):

  horarios = ['03:00', '09:00', '15:00', '21:00']
  if ling_graf == 'pt':
    label = f'Horário {horario}'
  elif ling_graf == 'en':
    label = f'Hour {horario}'
    estacao = ti.trad_para_ingles(estacao)
    horario = ti.trad_para_ingles(horario)
    componente_velocidade = ti.trad_para_ingles(componente_velocidade)
    ano = ti.trad_para_ingles(ano)

  # Verifica o tipo de gráfico a ser gerado
  if grafico == 'original':

    # Gera um gráfico de dispersão para os dados originais
    ax.scatter(X, Y, color=cor)
    # Plota uma linha suavizada usando os valores interpolados de X e Y
    ax.plot(X_smooth, Y_smooth, color=cor, label=label, linestyle='-')

    # Configuração do título e do eixo X de acordo com o tipo de dado (velocidade ou temperatura)
    if variavel == 'velocidade':
      if data == None:
        if ling_graf == 'pt':
          ax.set_title(f'Perfil de Velocidade do Vento - {plataforma} - Est: {estacao} - Ano: {ano} - Dir: {componente_velocidade}')  # Define o título para perfis de velocidade em português
        elif ling_graf == 'en':
          ax.set_title(f'Wind Profile - {plataforma} - Est: {estacao} - Year: {ano} - Dir: {componente_velocidade}')  # Define o título para perfis de velocidade em inglês
      else:
        if ling_graf == 'pt':
          ax.set_title(f'Perfil de Velocidade do Vento - {plataforma} - Est: {estacao} - Data: {data} - Dir: {componente_velocidade}')  # Define o título para perfis de velocidade em português
        elif ling_graf == 'en':
          ax.set_title(f'Wind Profile - {plataforma} - Est: {estacao} - Date: {data} - Dir: {componente_velocidade}')  # Define o título para perfis de velocidade em inglês
      if ling_graf == 'pt':
        ax.set_xlabel('Velocidade do Vento (m/s)')  # Nome do eixo X para velocidade em português
      elif ling_graf == 'en':
        ax.set_xlabel('Wind Speed (m/s)')  # Nome do eixo X para velocidade em inglês
    elif variavel == 'temperatura':
      if data == None:
        if ling_graf == 'pt':
          ax.set_title(f'Perfil de Temperatura - {plataforma} - Est: {estacao} - Ano: {ano}')  # Define o título para perfis de temperatura em português
        elif ling_graf == 'en':
          ax.set_title(f'Temperature Profile - {plataforma} - Est: {estacao} - Year: {ano}')  # Define o título para perfis de temperatura em inglês
      else:
        if ling_graf == 'pt':
          ax.set_title(f'Perfil de Temperatura - {plataforma} - Est: {estacao} - Data: {data}')  # Define o título para perfis de temperatura em português
        elif ling_graf == 'en':
          ax.set_title(f'Temperature Profile - {plataforma} - Est: {estacao} - Date: {data}')  # Define o título para perfis de temperatura em inglês
      if ling_graf == 'pt':
        ax.set_xlabel('Temperatura (°C)')  # Nome do eixo X para temperatura em português
      elif ling_graf == 'en':
        ax.set_xlabel('Temperature (°C)')  # Nome do eixo X para temperatura em inglês
  
  elif grafico == 'derivada':

    # Calcula a derivada dos dados suavizados (gradiente da variável X em relação a Y)
    derivada_X_smooth = np.gradient(X_smooth, Y_smooth)
    # Plota a derivada dos dados
    ax.plot(derivada_X_smooth, Y_smooth, color=cor, label=label, linestyle='--')

    # Adiciona uma linha vertical em x=0 depois do último horário (ex: 21:00)
    if horario == horarios[-1]:
      ax.axvline(x=0, color='black', linestyle='-', alpha=0.5, label='x = 0')  # Cria a linha vertical

    # Configuração do título e do eixo X de acordo com o tipo de dado (derivada de velocidade ou de temperatura)
    if variavel == 'velocidade':
      if data == None:
        if ling_graf == 'pt':
          ax.set_title(f'Derivada do Perfil de Velocidade - {plataforma} - Est: {estacao}) - Ano: {ano} - Dir: {componente_velocidade}')  # Título para derivada de velocidade
        elif ling_graf == 'en':
          ax.set_title(f'Derivative of Wind Profile - {plataforma} - Est: {estacao} - Year: {ano} - Dir: {componente_velocidade}')  # Título para derivada de velocidade
      else:
        if ling_graf == 'pt':
          ax.set_title(f'Derivada do Perfil de Velocidade - {plataforma} - Est: {estacao} - Data: {data} - Dir: {componente_velocidade}')  # Título para derivada de velocidade
        elif ling_graf == 'en':
          ax.set_title(f'Derivative of Wind Profile - {plataforma} - Est: {estacao} - Date: {data} - Dir: {componente_velocidade}')  # Título para derivada de velocidade
      if ling_graf == 'pt':
        ax.set_xlabel('Derivada da Velocidade do Vento')  # Nome do eixo X para derivada de velocidade
      elif ling_graf == 'en':
        ax.set_xlabel('Derivative of Wind Speed')  # Nome do eixo X para derivada de velocidade
    elif variavel == 'temperatura':
      if data == None:
        if ling_graf == 'pt':
          ax.set_title(f'Derivada do Perfil de Temperatura - {plataforma} - Est: {estacao} - Ano: {ano}')  # Título para derivada de temperatura
        elif ling_graf == 'en':
          ax.set_title(f'Derivative of Temperature Profile - {plataforma} - Est: {estacao} - Year: {ano}')
      else:
        if ling_graf == 'pt':
          ax.set_title(f'Derivada do Perfil de Temperatura - {plataforma} - Est: {estacao} - Data: {data}')  # Título para derivada de temperatura
        elif ling_graf == 'en':
          ax.set_title(f'Derivative of Temperature Profile - {plataforma} - Est: {estacao} - Date: {data}')
      if ling_graf == 'pt':
        ax.set_xlabel('Derivada da Temperatura') # Nome do eixo X para derivada de temperatura
      elif ling_graf == 'en':
        ax.set_xlabel('Derivative of Temperature') # Nome do eixo X para derivada de temperatura


  # Configurações comuns para os eixos dos gráficos (independente do tipo de dado)
  if ling_graf == 'pt':
    ax.set_ylabel('Altitude (m)') # Nome do eixo Y
  elif ling_graf == 'en':
    ax.set_ylabel('Height (m)') # Nome do eixo Y
  ax.grid(True)  # Adiciona uma grade ao gráfico
  ax.grid(True, which='both') # Habilita tanto a grade principal quanto a secundária
  ax.minorticks_on() # Ativa as marcas menores nos eixos
  ax.grid(which='minor', linestyle=':', linewidth=0.5) # Configura o estilo da grade menor (linhas pontilhadas e mais finas)
  ax.legend() # Adiciona uma legenda ao gráfico
