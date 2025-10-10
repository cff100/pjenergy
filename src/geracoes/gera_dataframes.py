import xarray as xr
from typing import cast
import dask.dataframe as dd
from pandas import DataFrame

from config.paths import Dataframes
from config.constants import Correspondencias as cr, Plataformas
from salvamentos.salva_dataframes import salva_dask_dataframe_parquet
from utils.representa_progresso import representa_progresso
from utils.obtem_dados_plataformas import plataforma_para_pasta_nome
from leituras.ler_arquivos_pastas_especificas import ler_datasets_pontuais_plataformas_geral
from edicoes.limpezas.remove_linhas_com_nan import remove_linhas_nan_dataframes



# FUNÇÔES AUXILIARES -------------------------------------------------------------------------------

def monta_dataframes_por_dimensao(ds: xr.Dataset) -> tuple[dd.DataFrame, DataFrame, DataFrame]:
    """Cria dataframes a partir de um dataset, separando variáveis 1D e 2D.
    
    Args:
        ds (xr.Dataset): Dataset contendo as variáveis a serem convertidas em dataframes.
        
    Returns:
        tuple[dd.DataFrame, DataFrame]: DataFrame Dask com variáveis 2D e DataFrame Pandas com variáveis 1D.
    """

    variaveis_2D = [v for v in ds.data_vars if ds[v].dims == (cr.DadosVariaveis.TEMPO_UTC0, cr.DadosVariaveis.ALTURA)]
    #print(f"Variáveis 2D: \n{variaveis_2D}")
    ds_2D = ds[variaveis_2D].chunk({cr.DadosVariaveis.TEMPO_UTC0: 200})
    df_2D = ds_2D.to_dask_dataframe()

    # Seleciona variáveis 1D (somente tempo) e monta um dataframe com elas
    variaveis_1D_tempo = [v for v in ds.data_vars if ds[v].dims == (cr.DadosVariaveis.TEMPO_UTC0,)]
    #print(f"Variáveis 1D: \n{variaveis_1D}")
    df_1D_tempo = ds[variaveis_1D_tempo].to_dataframe().reset_index()

    # Seleciona variáveis 1D (somente altura) e monta um dataframe com elas
    variaveis_1D_altura = [v for v in ds.data_vars if ds[v].dims == (cr.DadosVariaveis.ALTURA,)]
    #print(f"Variáveis 1D: \n{variaveis_1D}")
    df_1D_altura = ds[variaveis_1D_altura].to_dataframe().reset_index()

    print(f"1D_tempo: \n{df_1D_tempo.head()}\n\n")
    print(f"1D_altura: \n{df_1D_altura.head()}\n\n")
    print(f"2D: \n{df_2D.head()}")

    return df_2D, df_1D_tempo, df_1D_altura


def merge_dataframes_no_tempo(df_2D: dd.DataFrame, df_1D_tempo: DataFrame, df_1D_altura) -> dd.DataFrame:
    """Realiza o merge dos dataframes Dask e Pandas com base no tempo.

    Args:
        df_2D (dd.DataFrame): DataFrame Dask com variáveis 2D.
        df_1D_tempo (DataFrame): DataFrame Pandas com variáveis 1D (tempo).
        df_1D_altura (DataFrame): DataFrame Pandas com variáveis 1D (altura).
    Returns:
        dd.DataFrame: DataFrame Dask resultante do merge, contendo todas as variáveis
        com base no tempo.
    """

    # Para evitar que no merge ocorra a duplicação de coluna existente em dois dataframes 
    df_1D_tempo = df_1D_tempo.drop(columns=["tempo_bras"], errors="ignore")
    
    # Merge dos dataframes com base no tempo
    df_2D = df_2D.reset_index()
    df = df_2D.merge(df_1D_tempo, on=cr.DadosVariaveis.TEMPO_UTC0, how="left") # Merge com base no tempo
    df = df.merge(df_1D_altura, on=cr.DadosVariaveis.ALTURA, how="left") # Merge com base na altura


    return df


# FUNÇÔES INTERMEDIÁRIAS -------------------------------------------------------------------------------


def nc_para_dask_dataframe_simples(plataforma: str) -> dd.DataFrame:
    """Converte NetCDF em Dask DataFrame, salvando como parquet, preservando variáveis 1D e 2D.

    Args:
        plataforma (str): Nome da plataforma cujo caminho dos dados se deseja obter.

    Returns:
        dd.DataFrame: DataFrame Dask resultante da conversão.
    """

    ds = ler_datasets_pontuais_plataformas_geral(plataforma)
    
    nome_pasta = plataforma_para_pasta_nome(plataforma)
    df_caminho = Dataframes.DIRETORIO_PLATAFORMAS_GERAL / nome_pasta

    df_2D, df_1D_tempo, df_1D_altura = monta_dataframes_por_dimensao(ds)

    df = merge_dataframes_no_tempo(df_2D, df_1D_tempo, df_1D_altura)

    print(df.compute())

    df = df[cr.DadosVariaveis.NOVA_ORDEM_COLUNAS]

    df = remove_linhas_nan_dataframes(df)

    salva_dask_dataframe_parquet(df, df_caminho)

    return df



# FUNÇÃO PRINCIPAL -------------------------------------------------------------------------------


def nc_para_dask_dataframe_plataformas() -> dd.DataFrame:
    """Converte NetCDF de todas plataformas em Dask DataFrame, salvando como parquet."""

    print("--- CRIAÇÃO DE DATAFRAME(S) ---\n\n")

    plataformas = Plataformas.PLATAFORMAS # Lista de plataformas
    i = 1

    for plat in plataformas:
        print(f" -> -> -> Plataforma: {plat} ({representa_progresso(i, plataformas)})\n")
        df = nc_para_dask_dataframe_simples(plat)
        i += 1

    print("Todos os dataframes foram salvos!\n")

    df = cast(dd.DataFrame, df)
    
    return df  # Retorna o dataframe da última plataforma


if __name__ == "__main__":
    df = nc_para_dask_dataframe_plataformas()