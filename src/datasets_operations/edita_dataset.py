from pathlib import Path
import pandas as pd
import numpy as np
import xarray as xr
from datasets_operations.ler_nc import ler_dataset_nc
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO, CAMINHO_ABSOLUTO_DATASET_EDITADO
from config.constants import NomeColunasDataframe as ncd, ConstantesNumericas as cn, ConstantesString as cs, OutrasConstantes as oc
from datasets_operations.salva_dataset import salva_dataset_nc

# FUNÇÕES AUXILIARES ---------------------------------------


def dataset_adiciona_estacao_do_ano(dataset: xr.Dataset) -> xr.Dataset:
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
        for estacao, intervalo in oc.estacao_do_ano_dados.items(): # intervalo: representa o dicionário aninhado que contém o dia e mês de início e fim da específica estação do ano
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
    ds = dataset.assign({ncd.estacao_do_ano: (ncd.tempo_bras, np.array(estacoes))})
    return ds


# FUNÇÕES INTERMEDIÁRIAS ---------------------------------------

def dataset_remocoes(dataset:xr.Dataset) -> xr.Dataset:
    "Remove coordenadas e variáveis indesejadas"

    lista_remover = ['number', 'expver']
    ds = dataset.drop_vars(lista_remover)

    return ds


def dataset_interpola_lat_lon(dataset: xr.Dataset, latitude_longitude_alvo: tuple[float, float]) -> xr.Dataset:
    """Faz a interpolação das variáveis na longitude e latitude"""

    # Verifica se os pontos de latitude e longitude estão dentro do intervalo do dataset
    if not (dataset.latitude.min() <= latitude_longitude_alvo[0] <= dataset.latitude.max() and
            dataset.longitude.min() <= latitude_longitude_alvo[1] <= dataset.longitude.max()):
        raise ValueError(f"Os pontos de latitude {latitude_longitude_alvo[0]} e longitude {latitude_longitude_alvo[1]} estão fora do intervalo do dataset.")
    
    # Interpola as variáveis
    variaveis_lista = list(dataset.data_vars) # Variáveis a serem interpoladas
    ds_interp = dataset[variaveis_lista].interp(latitude=latitude_longitude_alvo[0], longitude = latitude_longitude_alvo[1], method="linear")

    return ds_interp



def dataset_criacoes(dataset: xr.Dataset) -> xr.Dataset:
    "Criar variáveis no dataset"

    # Cria variável de altura
    dataset["h"] = dataset["z"] / cn.g

    # Cria variável de velocidade resultante
    dataset[ncd.velocidade_resultante] = (dataset["u"]**2 + dataset["v"]**2) ** 0.5

    # Cria variável de temperatura em celsius
    dataset[ncd.temperatura_celsius] = dataset["t"] - 273.15

    # Cria coordenada de tempo no UTC-3
    nome_datetime = "valid_time"
    tempo_bras = pd.to_datetime(dataset[nome_datetime].values).tz_localize("UTC").tz_convert("Etc/GMT+3").tz_localize(None)
    ds = dataset.assign_coords({ncd.tempo_bras: (nome_datetime, tempo_bras)})

    
    
    # Cria coordenadas temporais separadas em partes a partir do datatime no horário de Brasília
    ano = ds[ncd.tempo_bras].dt.year
    mes = ds[ncd.tempo_bras].dt.month
    mes_str = mes.copy(data=[oc.numero_para_mes[int(m)] for m in mes.values])
    dia = ds[ncd.tempo_bras].dt.day
    hora = ds[ncd.tempo_bras].dt.hour
    hora_str = ds[ncd.tempo_bras].dt.strftime("%H:00")

    dados = {"ano": ano, "mes": mes, "mes_str": mes_str, "dia": dia, "hora": hora, "hora_str": hora_str}

    ds = ds.assign(dados)

    ds = dataset_adiciona_estacao_do_ano(ds)

    return ds


def dataset_renomeacoes(dataset: xr.Dataset) -> xr.Dataset:
    "Renomeia coordenadas/variáveis"

    dicionario_renomear = ncd.novos_nomes
    ds = dataset.rename(dicionario_renomear)

    return ds


# FUNÇÃO PRINCIPAL ---------------------------------------

def edita_dataset_unico(latitude_longitude_alvo: tuple[float, float], caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO, 
                        caminho_absoluto_dataset_editado: Path = CAMINHO_ABSOLUTO_DATASET_EDITADO) -> xr.Dataset:
    "Faz edições no nomes e gera variáveis e coordenadas."

    # Lê dataset (verificando se o dataset existe)
    ds = ler_dataset_nc(caminho_relativo_dataset_unico)

    processos = [dataset_remocoes, dataset_interpola_lat_lon, dataset_criacoes, dataset_renomeacoes]

    for funcao in processos:
        if funcao == dataset_interpola_lat_lon:
            ds = funcao(ds, latitude_longitude_alvo)
        else:
            ds = funcao(ds)

    salva_dataset_nc(ds, caminho_absoluto_dataset_editado)

    return ds


if __name__ == "__main__":
    ds = edita_dataset_unico((-22.0, -40.0))
    print(ds)







