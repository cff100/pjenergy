def plot_weibull_velocidade(pressao, estacao, ano):

  fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Cria uma grade 2x2 para os gráficos
  tabela_probabilidades = pd.DataFrame()

  for i, horario in enumerate(horarios):
      # Filtrar os dados por horário
      df_horario = df[df['Horário_Brasília'] == horario]['Velocidade_Vento_resultante_m/s']

      # Verificar se existem dados suficientes para o horário
      if df_horario.empty:
          print(f'Nenhum dado disponível para {horario}')
          continue

      # Ajustar a distribuição de Weibull
      params = weibull_min.fit(df_horario)
      shape, loc, scale = params

      # Gerar pontos para a função CDF
      x = np.linspace(min(df_horario), max(df_horario), 100)
      weibull_cdf = weibull_min.cdf(x, shape, loc, scale)

      # Seleciona o eixo correspondente
      ax = axs[i//2, i % 2]

      # Plotar a CDF no gráfico
      ax.plot(x, weibull_cdf, label=f'CDF Weibull ({horario})', color='b')
      ax.set_xlabel('Velocidade do Vento (m/s)')
      ax.set_ylabel('Probabilidade Acumulada')

      if pressao or estacao:
        if not estacao:
          ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Pressão: {pressao} hPa')
        elif not pressao:
          ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Estação: {estacao}')
        else:
          ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Pressão: {pressao} hPa - Estação: {estacao}')
      else:
        ax.set_title(f'Ajuste de Distribuição Weibull - {horario}')

      ax.grid(True)  # Grid para major e minor ticks
      ax.minorticks_on()  # Habilitar minor ticks
      ax.grid(True, which='minor', alpha=0.3)

      if mediana_show == True:

        # Calcular a mediana (probabilidade acumulada = 0.5)
        mediana = weibull_min.ppf(0.5, shape, loc, scale)

        # Marcar a mediana no gráfico
        ax.axvline(x=mediana, color='g', linestyle='-', label=f'Mediana: {mediana:.2f}m/s')
        ax.text(mediana, 0.5, f'{mediana:.2f}', color='g', ha='right')

      if valor_especifico is not None:
        # Marcar o valor específico no gráfico e sua probabilidade
        probabilidade_especifica = weibull_min.cdf(valor_especifico, shape, loc, scale)
        ax.axvline(x=valor_especifico, color='r', linestyle='--', label=f'P(x ≤ {valor_especifico} m/s)')
        ax.text(valor_especifico, probabilidade_especifica, f'{probabilidade_especifica:.2f}', color='r', ha='right')

      # Adicionar a probabilidade ao gráfico
      ax.legend()

      # Criar uma tabela com as probabilidades
      df_tabela = pd.DataFrame({
          'Velocidade do Vento (m/s)': x,
          'Probabilidade Acumulada (CDF)': weibull_cdf
      })
      df_tabela['Horário'] = horario
      tabela_probabilidades = pd.concat([tabela_probabilidades, df_tabela], ignore_index=True)

  # Ajustar o espaçamento entre os subplots
  plt.tight_layout()
  plt.show()

  print('\n')

  if nome_tabela:
    nome_tabela = '_' + nome_tabela
  else:
    nome_tabela = ''

  # Salvar a tabela em um arquivo CSV, se desejado
  tabela_probabilidades.to_csv(f'Velocidade_Tabela_probabilidades_CDF_weibull{nome_tabela}.csv', index=False)
