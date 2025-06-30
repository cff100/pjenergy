import dask.dataframe as dd
from pathlib import Path
# Módulos internos do projeto
from config.paths import DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS

def ler_dataframe_dask(diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Ler o dataframe dask composto por arquivos parquet."""
    
    df = dd.read_parquet(diretorio_dados_parquet)
    return df


# VER OS DADOS (INCLUINDO TODAS PARTIÇÕES)

def n_primeiras_linhas(n: int = 5, diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Mostras as n primeiras linhas."""

    df = ler_dataframe_dask(diretorio_dados_parquet)
    head = df.compute().head(n)
    return head

def ler_ultimas_linhas(n: int = 5, diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Mostras as n últimas linhas."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    tail = df.compute().tail(n)
    return tail

def amostra_aleatoria(frac: float = 0.001, diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Pega uma amostra aleatória de uma quantidade especificada de linhas do dataframe."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    amostra = df.sample(frac = frac).compute()
    return amostra

def acessa_particao_especifica(particao: int = 0, diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Pega uma amostra aleatória de uma quantidade especificada de linhas do dataframe."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    particao = df.partitions[particao].compute()
    return particao
    
# OBTER INFORMAÇÕES DE TIPOS, COLUNAS, DTYPES, ETC

def lista_nomes_colunas(diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Retorna os nomes das colunas do dataframe."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    colunas = df.columns.tolist()
    return colunas

def tipos_colunas(diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Retorna os tipos de dados das colunas do dataframe."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    tipos = df.dtypes
    return tipos

def numero_linhas_e_colunas(diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Retorna o número de linhas e colunas do dataframe."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    num_linhas = df.shape[0].compute()  # Computa o número de linhas
    num_colunas = df.shape[1]  # Número de colunas é uma propriedade
    return num_linhas, num_colunas

# INFORMAÇÕES ESTATÍSTICAS E ESTRUTURAIS    

def resumo_estatistico(diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Retorna um resumo estatístico do dataframe."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    resumo = df.describe().compute()
    return resumo

# OUTROS MÉTODOS ÚTEIS

def numero_particoes(diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Retorna o número de partições do dataframe."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    num_particoes = df.npartitions
    return num_particoes

from typing import Callable

def executa_em_cada_particao(funcao: Callable, diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """Executa uma função em cada partição do dataframe."""
    
    df = ler_dataframe_dask(diretorio_dados_parquet)
    resultados = df.map_partitions(funcao).compute()
    return resultados

if __name__ == "__main__":

    df = ler_dataframe_dask()

    head = n_primeiras_linhas(10)
    print(" -> -> -> head:")
    print(head)
    print("\n")

    tail = ler_ultimas_linhas()
    print(" -> -> -> tail:")
    print(tail)
    print("\n")

    # amostra = amostra_aleatoria(frac=0.0001)
    # print(amostra.tail(100))

    # particao = acessa_particao_especifica()
    # print(particao)

    # colunas = lista_nomes_colunas()
    # print(colunas)

    # tipos = tipos_colunas(DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS)
    # print(tipos)

    # num_linhas, num_colunas = numero_linhas_e_colunas()
    # print(num_linhas, num_colunas)

    # resumo = resumo_estatistico()
    # print(resumo)

    # num_particoes = numero_particoes()
    # print(num_particoes)

    # resultados = executa_em_cada_particao(lambda part: part.tail(1))
    # print(resultados)

    # df = ler_dataframe_dask(DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS)
    # #print(df["ano"].unique().compute())
    # #print(df.tail())
    # df_mes = df[df["hora"] == "03:00"].compute()
    # print(df_mes.tail())