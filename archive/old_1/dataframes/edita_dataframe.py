from pathlib import Path
import dask.dataframe as dd
from dask.diagnostics.progress import ProgressBar
import pytz
# Módulos internos do projeto
from datasets_operations.dataframes.ler_dataframe import ler_dataframe_dask
from datasets_operations.dataframes.salva_dataframe_substituindo import salva_dataframe_substituindo
from config.paths import DIRETORIO_DATAFRAME_PRIMARIO, DIRETORIO_DATAFRAME_NOVAS_COLUNAS
from config.constants import CorrespondeNomesDados as ncd
from config.constants import ConstantesNumericas as cn
from config.constants import OutrasConstantes as oc, Correspondencias as cr
from utils.decide_estacao import decide_estacao_vetorizado

def copia_dataframe_primario(diretorio_dataframe_primario: Path = DIRETORIO_DATAFRAME_PRIMARIO, diretorio_dataframe_novas_colunas: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS):
    """Faz uma cópia da pasta do dataframe primário na pasta de dataframe com novas colunas. Serve para iniciar a modificação das colunas."""

    # Lê o dataframe primario
    df = ler_dataframe_dask(diretorio_dataframe_primario)

    # Salva na pasta que será usada
    with ProgressBar(): # Com barra de progresso no terminal
        print("Copiando dataframe primário para pasta que terá o dataframe com colunas editadas...")
        df.to_parquet(diretorio_dataframe_novas_colunas, overwrite = True)
        print("\n")


def remover_colunas_indesejadas(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    df = df.drop(columns = [ncd.number, ncd.exp_ver])

    # Salva dataframe substituindo o original
    print("Removendo colunas indesejadas...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df

def renomear_colunas(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    "Renomeia nome de algumas colunas"

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    # Renomeia as colunas
    df = df.rename(columns=ncd.novos_nomes)

    # Salva dataframe substituindo o original
    print("Renomeando colunas...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df

def adiciona_colunas_tempo(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """
    Lê um DataFrame Dask a partir de arquivos Parquet e adiciona colunas derivadas da coluna 'valid_time'.
    """

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    # Ajusta o horário para o fuso de Brasília (UTC-3). Desconsidera-se horário de verão para manter dados comparáveis em toda faixa de anos obtida.
    utc_3 = pytz.FixedOffset(-180)  # -180 minutos = UTC-3
    df[ncd.tempo_bras] = df[ncd.tempo_UTC0].dt.tz_localize("UTC").dt.tz_convert(utc_3)

    # Extrai componentes da data
    df[ncd.ano] = df[ncd.tempo_bras].dt.year
    df[ncd.mes] = df[ncd.tempo_bras].dt.month
    df[ncd.dia] = df[ncd.tempo_bras].dt.day
    df[ncd.hora] = df[ncd.tempo_bras].dt.hour.astype(str).str.zfill(2) + ":" + df[ncd.tempo_bras].dt.minute.astype(str).str.zfill(2)  # Formata a hora como string com dois dígitos
    
    # Converte número do mês para nome do mês
    df[ncd.mes_nome] = df[ncd.tempo_bras].dt.month.map(cr.DadosVariaveis.NUMERO_PARA_MES, meta=(ncd.mes_nome, "object"))
    
    ## Salva dataframe substituindo o original
    print("Adicionando colunas de tempo...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df

def adiciona_coluna_estacao(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    "Adiciona a coluna com os valores das estações do ano"

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    #df[ncd.estacao_do_ano_nome] = decide_estacao_vetorizado(df[ncd.dia], df[ncd.mes])

    df = df.map_partitions(
                                lambda d: d.assign(**{
                                    ncd.estacao_do_ano: decide_estacao_vetorizado(d[ncd.dia], d[ncd.mes])
                                })
                            )

    ## Salva dataframe substituindo o original
    print("Adicionando coluna de estações do ano...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df


def adiciona_coluna_velocidade_resultante(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """Calcula e adiciona uma coluna de velocidade resultante"""

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    # Cria a coluna de velocidade resultante
    df[ncd.velocidade_resultante] = (df[ncd.velocidade_u]**2 + df[ncd.velocidade_v]**2)**0.5

    # Salva dataframe substituindo o original
    print("Adicionando colunas velocidade resultante...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df

def adiciona_coluna_altura(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    # Cria a coluna de altura a partir do geopotencial (h = z / g)
    df[ncd.altura] = df[ncd.geopotencial] / cn.g

    # Salva dataframe substituindo o original
    print("Adicionando coluna de altura...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df


def adiciona_coluna_temperatura_celsius(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """Adiciona uma coluna de temperatura a partir da coluna de temperatura em celsius"""

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    df[ncd.temperatura_celsius] = df[ncd.temperatura_kelvin] - 273.15

    # Salva dataframe substituindo o original
    print("Adicionando coluna de temperatura em graus celsius...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df

def ordena_colunas(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """Ordena as colunas do dataframe"""

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    df = df[ncd.lista_colunas_ordem]

    # Salva dataframe substituindo o original
    print("Reordenando colunas...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df


# FUNÇÃO PRINCIPAL

def edita_colunas() -> dd.DataFrame:
    """Cria um dataframe com colunas novas"""

    # Lista de funções que executam cada parte do processo
    processos = [copia_dataframe_primario, 
                 remover_colunas_indesejadas, 
                 renomear_colunas,
                 adiciona_colunas_tempo,
                 adiciona_coluna_estacao,
                 adiciona_coluna_velocidade_resultante, 
                 adiciona_coluna_altura, 
                 adiciona_coluna_temperatura_celsius, 
                 ordena_colunas]

    # Execução ordenada das funções
    for funcao in processos:
        df = funcao()

    return df


if __name__ == "__main__":
    # Executa a função para adicionar colunas de tempo
    df = edita_colunas()

    # Exibe as primeiras linhas do DataFrame atualizado
    print(df.compute())
    