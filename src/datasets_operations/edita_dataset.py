from pathlib import Path
import pandas as pd
import numpy as np
import xarray as xr
from datasets_operations.ler_nc import ler_dataset_nc_relativo
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO, decide_caminho_absoluto_dataset_localizacao_especifica
from config.constants import CorrespondeNomesDados as ncd, ConstantesNumericas as cn,  OutrasConstantes as oc
from datasets_operations.salva_dataset import salva_dataset_nc
from utils.gerencia_plataformas_representacoes import gerencia_plataforma_nome

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
    ds = dataset.assign({ncd.estacao_do_ano: (ncd.tempo_UTC0, np.array(estacoes))})
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
        raise ValueError(
            f"Os pontos de latitude {latitude_longitude_alvo[0]} e longitude {latitude_longitude_alvo[1]} estão fora do intervalo do dataset. Mínimo: ({dataset.latitude.min().item()},{dataset.longitude.min().item()}) - Máximo: ({dataset.latitude.max().item()},{dataset.longitude.max().item()})"
            )
    
    # Interpola as variáveis
    #variaveis_lista = list(dataset.data_vars) # Variáveis a serem interpoladas
    ds_interp = dataset.interp(latitude=latitude_longitude_alvo[0], longitude = latitude_longitude_alvo[1], method="linear")

    # Remove as dimensões de latitude e longitude
    for dim in ["latitude", "longitude"]:
        if dim in ds_interp.dims:
            ds_interp = ds_interp.squeeze(dim)
        if dim in ds_interp.coords or dim in ds_interp.variables:
            ds_interp = ds_interp.drop_vars(dim)
            
    return ds_interp


def interp_alturas_constantes(ds: xr.Dataset) -> xr.Dataset:
    """
    Interpola as variáveis do dataset para alturas constantes em metros,
    convertendo os níveis de pressão para alturas usando o geopotencial.

    Retorna um novo Dataset com variáveis em função de altura e tempo,
    e com a pressão estimada como variável interpolada.
    """

    # -----------------------------
    # ETAPA 1: Definir alturas alvo
    # -----------------------------
    # Essas são as alturas (em metros) para as quais queremos valores interpolados.
    alturas_desejadas = np.arange(25, 401, 25)

    # -----------------------------
    # ETAPA 2: Calcular altura a partir do geopotencial
    # -----------------------------
    # O geopotencial 'z' tem unidade m²/s². Ao dividir pela aceleração da gravidade,
    # obtemos a altura geométrica (em metros): h = z / g.
    # Isso resulta em um DataArray com dimensões (valid_time, pressure_level).
    h = ds["z"] / cn.g

    # -----------------------------
    # ETAPA 3: Identificar variáveis a serem interpoladas
    # -----------------------------
    # Seleciona apenas variáveis com as dimensões exatas (valid_time, pressure_level),
    # que são as variáveis que fazem sentido serem interpoladas verticalmente.
    variaveis = [
        var for var in ds.data_vars
        if set(ds[var].dims) == {"valid_time", "pressure_level"}
    ]

    # Inicializa um novo Dataset que irá armazenar os resultados interpolados
    ds_interp = xr.Dataset()

    # -----------------------------
    # ETAPA 4: Função auxiliar de interpolação 1D
    # -----------------------------
    # Essa função recebe vetores 1D de altura (h) e da variável (var),
    # e retorna os valores da variável interpolados para as alturas desejadas.
    def interp_1d(h_vals, var_vals, alturas):
        # Ordena os valores de altura (por segurança)
        ordenado = np.argsort(h_vals)
        # Interpola usando np.interp (linear por padrão)
        return np.interp(alturas, h_vals[ordenado], var_vals[ordenado])

    # -----------------------------
    # ETAPA 5: Aplicar interpolação nas variáveis
    # -----------------------------
    # Para cada variável relevante do Dataset:
    for var in variaveis:
        # Aplica a função de interpolação com xarray.apply_ufunc,
        # o que permite operação vetorizada (e com dask se disponível).
        da_interp = xr.apply_ufunc(
            interp_1d,              # Função que será aplicada
            h,                      # Altura real calculada (como base para interpolação)
            ds[var],                # Dados da variável a interpolar
            input_core_dims=[["pressure_level"], ["pressure_level"]],
            output_core_dims=[["altura"]],
            vectorize=True,         # Aplica elemento a elemento nos outros eixos (ex: tempo)
            dask="parallelized",    # Permite processamento paralelo com Dask
            kwargs={"alturas": alturas_desejadas},  # Alturas alvo
            output_dtypes=[ds[var].dtype],          # Tipo de saída
        )
        # Armazena no novo dataset
        ds_interp[var] = da_interp

    # -----------------------------
    # ETAPA 6: Interpolar também a pressão
    # -----------------------------
    # A pressão é originalmente uma coordenada, mas aqui queremos que ela vire uma variável,
    # representando a pressão estimada correspondente às alturas desejadas.
    # Para isso, usamos a mesma técnica de interpolação.
    pressao_vals = ds["pressure_level"]

    # Como 'pressure_level' não depende do tempo, usamos broadcast_like(h)
    # para replicar os valores de pressão ao longo da dimensão 'valid_time'
    da_pressao_interp = xr.apply_ufunc(
        interp_1d,
        h,                                 # altura (h) calculada  / 1º argumento -> h_vals → ["pressure_level"]
        pressao_vals.broadcast_like(h),    # pressão replicada no tempo / 2º argumento -> var_vals → ["pressure_level"]
        input_core_dims=[["pressure_level"], ["pressure_level"]],
        output_core_dims=[["altura"]],
        vectorize=True,
        dask="parallelized",
        kwargs={"alturas": alturas_desejadas},
        output_dtypes=[pressao_vals.dtype],
    )

    # Adiciona a pressão como uma nova variável no dataset resultante
    ds_interp["pressure_level"] = da_pressao_interp

    # -----------------------------
    # ETAPA 7: Adicionar coordenada de altura
    # -----------------------------
    # Para fins de organização, adicionamos explicitamente a coordenada 'altura'
    ds_interp = ds_interp.assign_coords(altura=("altura", alturas_desejadas))

    # -----------------------------
    # ETAPA 8: Reorganizar as dimensões
    # -----------------------------
    # Garante que as dimensões fiquem na ordem desejada: (tempo, altura)
    ds_interp = ds_interp.transpose("valid_time", "altura")

    return ds_interp


def dataset_criacoes(dataset: xr.Dataset) -> xr.Dataset:
    "Criar variáveis no dataset"

    # Cria variável de altura
    #dataset["h"] = dataset["z"] / cn.g

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
    mes_str = mes.copy(data=[oc.NUMERO_PARA_MES[int(m)] for m in mes.values])
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


# FUNÇÕES PRINCIPAIS ---------------------------------------

def cria_datasets_plataformas(caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> None:

    for plat in list(oc.plataformas_dados.keys()):
        print(f"Plataforma: {plat}")
        cria_dataset_ponto_especifico(plataforma = plat, caminho_relativo_dataset_unico = caminho_relativo_dataset_unico)



def cria_dataset_ponto_especifico(plataforma: str | None = None, 
                                  latitude_longitude_alvo: tuple[float, float] | None = None, 
                                  caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> xr.Dataset:
    "Faz edições no dataset único para criar um dataset para um ponto específico"

    if not plataforma and not latitude_longitude_alvo:
        raise ValueError("É necessário informar a latitude e longitude alvo ou a plataforma.")
    
    elif plataforma:
            
        plataforma = gerencia_plataforma_nome(plataforma)

        if not latitude_longitude_alvo: # Caso seja escolhida uma plataforma específica e as coordenadas não seja dadas, é obtido os valores das coordenadas dela.
            latitude_longitude_alvo = oc.plataformas_dados[plataforma]["coords"]
        elif latitude_longitude_alvo:
            # Confere se as coordenadas dadas correspondem à plataforma escolhida
            if latitude_longitude_alvo != oc.plataformas_dados[plataforma]["coords"]:
                latitude_longitude_alvo = oc.plataformas_dados[plataforma]["coords"]
                print(f"Sobreescrevendo as coordenadas fornecidas para as coordenadas reais da plataforma fornecida: {latitude_longitude_alvo}\n")
            else:
                pass
    # Lê dataset (verificando se o dataset existe)
    ds = ler_dataset_nc_relativo(caminho_relativo_dataset_unico)

    processos = [dataset_remocoes, dataset_interpola_lat_lon, interp_alturas_constantes, dataset_criacoes, dataset_renomeacoes]

    for funcao in processos:
        if funcao == dataset_interpola_lat_lon:
            ds = funcao(ds, latitude_longitude_alvo)
        else:
            ds = funcao(ds)

    salva_dataset_nc(ds, decide_caminho_absoluto_dataset_localizacao_especifica(plataforma))

    return ds


def cria_datasets_especificos_alternativas(alternativa_plataforma: str | None = None, 
                                           latitude_longitude_alvo: tuple[float, float] | None = None, 
                                           caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> None | xr.Dataset :
    """Escolhe a função de criar dataset a ser chamada dependendo da escolha de todas as plataformas (alternativa_plataforma = 'all') ou 
    um ponto específico (alternativa_plataforma = None)"""
    
    if alternativa_plataforma == "all":
        cria_datasets_plataformas(caminho_relativo_dataset_unico = caminho_relativo_dataset_unico)
    elif alternativa_plataforma == None:
        ds = cria_dataset_ponto_especifico(latitude_longitude_alvo = latitude_longitude_alvo, 
                                           caminho_relativo_dataset_unico = caminho_relativo_dataset_unico)
        return ds 




if __name__ == "__main__":
    #ds = cria_datasets_especificos_alternativas("p5", (-22.0, -40.0))
    #ds = cria_datasets_especificos_alternativas(latitude_longitude_alvo=(-22.0, -40.0))
    #print(ds)
    #cria_datacria_datasets_especificos_alternativas()
    cria_datasets_especificos_alternativas(latitude_longitude_alvo=(-22.0, -40.0))
    







