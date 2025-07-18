import xarray as xr
import numpy as np
import pandas as pd
from config.constants import OutrasConstantes as oc, Correspondencias as cr

def adiciona_estacao_do_ano(dataset: xr.Dataset) -> xr.Dataset:
    """Adiciona a variável 'estacao' ao dataset com base nas colunas 'mes' e 'dia'.

    Args:
        dataset (xarray.Dataset): Dataset que deve conter 'mes' e 'dia' como variáveis.

    Returns:
        xarray.Dataset: Dataset com a variável 'estacao'.
    """

    # Pega os valores de mes e dia em arrays numpy
    meses = dataset["mes"].values  
    dias = dataset["dia"].values

    estacoes = []

    # Percorre todos os pares mês e dia para dar a cada um valor de estação correspondente 
    for mes, dia in zip(meses, dias): 
        # Percorre as estações
        for estacao, intervalo in oc.ESTACAO_DO_ANO_DATAS.items(): # intervalo: representa o dicionário aninhado que contém o dia e mês de início e fim da específica estação do ano
            inicio = intervalo["inicio"]
            fim = intervalo["fim"]

            # Estações que não cruzam o ano
            if inicio["mes"] < fim["mes"]:
                if ((mes > inicio["mes"] and mes < fim["mes"]) or       # Nos dois meses entre os meses de iníco e fim da estação
                    (mes == inicio["mes"] and dia >= inicio["dia"]) or  # No mês de início, a partir do dia de início da estação
                    (mes == fim["mes"] and dia <= fim["dia"])):         # No mês de fim, até o dia do fim da estação
                    estacoes.append(estacao)
                    break
            # Estação que cruza o ano (Verão)
            else:
                if ((mes < fim["mes"]) or                               # Nos dois meses entre os meses de iníco e fim da estação (Janeiro e Fevereiro)
                    (mes == inicio["mes"] and dia >= inicio["dia"]) or  # No mês de início (Dezembro), a partir do dia de início da estação
                    (mes == fim["mes"] and dia <= fim["dia"])):         # No mês de fim (Março), até o dia do fim da estação
                    estacoes.append(estacao)
                    break


    # Cria a nova variável
    ds = dataset.assign({cr.DadosVariaveis.ESTACAO_DO_ANO: (cr.DadosVariaveis.TEMPO_UTC0, np.array(estacoes))})

    return ds



def adiciona_variaveis(dataset: xr.Dataset) -> xr.Dataset:
    """Criar diversas variáveis/coordenadas no dataset. 
    
    Cria as variáveis de velocidade resultante, temperatura em Celsius,
    e coordenadas temporais separadas (ano, mes, mes_str, dia, hora, hora_str) a partir do tempo UTC-3, 
    além de chamar a função de adição da estação do ano.
    
    Args:
        dataset (xarray.Dataset): Dataset a ter variáveis/coordenadas adicionadas.

    Returns:
        xarray.Dataset: Dataset com a variáveis/coordenadas adicionadas.
    """


    # Cria variável de velocidade resultante
    dataset[cr.DadosVariaveis.VELOCIDADE_RESULTANTE] = (dataset["u"]**2 + dataset["v"]**2) ** 0.5

    # Cria variável de temperatura em celsius
    dataset[cr.DadosVariaveis.TEMPERATURA_CELSIUS] = dataset["t"] - 273.15

    # Cria coordenada de tempo no UTC-3
    nome_datetime = "valid_time"
    # Converte os valores do tempo para objetos datetime do pandas
    tempo_bras = pd.to_datetime(dataset[nome_datetime].values)
    # Define o fuso horário como UTC
    tempo_bras = tempo_bras.tz_localize("UTC")
    # Converte o fuso horário de UTC para o horário de Brasília (UTC-3)
    tempo_bras = tempo_bras.tz_convert("Etc/GMT+3")
    # Remove a informação de fuso horário, deixando os datetimes como "naive"
    tempo_bras = tempo_bras.tz_localize(None)
    ds = dataset.assign_coords({cr.DadosVariaveis.TEMPO_BRAS: (nome_datetime, tempo_bras)})

    
    
    # Cria coordenadas temporais separadas em partes a partir do datatime no horário de Brasília
    ano = ds[cr.DadosVariaveis.TEMPO_BRAS].dt.year
    mes = ds[cr.DadosVariaveis.TEMPO_BRAS].dt.month
    mes_str = mes.copy(data=[cr.DadosVariaveis.NUMERO_PARA_MES[int(m)] for m in mes.values])
    dia = ds[cr.DadosVariaveis.TEMPO_BRAS].dt.day
    hora = ds[cr.DadosVariaveis.TEMPO_BRAS].dt.hour
    hora_str = ds[cr.DadosVariaveis.TEMPO_BRAS].dt.strftime("%H:00")

    dados = {"ano": ano, "mes": mes, "mes_str": mes_str, "dia": dia, "hora": hora, "hora_str": hora_str}

    ds = ds.assign(dados)

    ds = adiciona_estacao_do_ano(ds)

    return ds
