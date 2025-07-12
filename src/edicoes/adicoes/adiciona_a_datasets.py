import xarray as xr
import numpy as np
import pandas as pd
from config.constants import OutrasConstantes as oc, Correspondencias as cr

def adiciona_estacao_do_ano(dataset: xr.Dataset) -> xr.Dataset:
    """
    Adiciona a variável 'estacao' ao Dataset com base nas colunas 'mes' e 'dia'.

    Parâmetros:
        dataset (xarray.Dataset): Deve conter 'mes' e 'dia' como variáveis.

    Retorna:
        xarray.Dataset com a variável 'estacao'.
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
                if ((mes > inicio["mes"] and mes < fim["mes"]) or
                    (mes == inicio["mes"] and dia >= inicio["dia"]) or
                    (mes == fim["mes"] and dia <= fim["dia"])):
                    estacoes.append(estacao)
                    break
            # Estação que cruza o ano - Verão
            else:
                if ((mes > inicio["mes"] or mes < fim["mes"]) or
                    (mes == inicio["mes"] and dia >= inicio["dia"]) or
                    (mes == fim["mes"] and dia <= fim["dia"])):
                    estacoes.append(estacao)
                    break


    # Cria a nova variável
    ds = dataset.assign({cr.ESTACAO_DO_ANO: (cr.TEMPO_UTC0, np.array(estacoes))})
    return ds



def adiciona_variaveis(dataset: xr.Dataset) -> xr.Dataset:
    "Criar variáveis/coordenadas no dataset"


    # Cria variável de velocidade resultante
    dataset[cr.VELOCIDADE_RESULTANTE] = (dataset["u"]**2 + dataset["v"]**2) ** 0.5

    # Cria variável de temperatura em celsius
    dataset[cr.TEMPERATURA_CELSIUS] = dataset["t"] - 273.15

    # Cria coordenada de tempo no UTC-3
    nome_datetime = "valid_time"
    tempo_bras = pd.to_datetime(dataset[nome_datetime].values).tz_localize("UTC").tz_convert("Etc/GMT+3").tz_localize(None)
    ds = dataset.assign_coords({cr.TEMPO_BRAS: (nome_datetime, tempo_bras)})

    
    
    # Cria coordenadas temporais separadas em partes a partir do datatime no horário de Brasília
    ano = ds[cr.TEMPO_BRAS].dt.year
    mes = ds[cr.TEMPO_BRAS].dt.month
    mes_str = mes.copy(data=[oc.NUMERO_PARA_MES[int(m)] for m in mes.values])
    dia = ds[cr.TEMPO_BRAS].dt.day
    hora = ds[cr.TEMPO_BRAS].dt.hour
    hora_str = ds[cr.TEMPO_BRAS].dt.strftime("%H:00")

    dados = {"ano": ano, "mes": mes, "mes_str": mes_str, "dia": dia, "hora": hora, "hora_str": hora_str}

    ds = ds.assign(dados)

    ds = adiciona_estacao_do_ano(ds)

    return ds
