import xarray as xr
from typing import cast
import dask.dataframe as dd
from pandas import DataFrame
from leituras.ler_arquivos import ler_arquivo
from config.paths import PathsDados as pad
from config.constants import FormatosArquivo as fa, Correspondencias as cr, Plataformas
from salvamentos.salva_dataframes import salva_dask_dataframe_parquet
from utils.representa_progresso import representa_progresso



# FUNÇÔES AUXILIARES -------------------------------------------------------------------------------

def monta_dataframes_por_dimensao(ds: xr.Dataset) -> tuple[dd.DataFrame, DataFrame]:

    variaveis_2d = [v for v in ds.data_vars if ds[v].dims == (cr.DadosVariaveis.TEMPO_UTC0, cr.DadosVariaveis.ALTURA)]
    ds_2d = ds[variaveis_2d].chunk({cr.DadosVariaveis.TEMPO_UTC0: 200})
    df = ds_2d.to_dask_dataframe()

    # Seleciona variáveis 1D (somente tempo) e monta um dataframe com elas
    variaveis_1d_str = [v for v in ds.data_vars if ds[v].dims == (cr.DadosVariaveis.TEMPO_UTC0,)]
    df_str = ds[variaveis_1d_str].to_dataframe().reset_index()

    return df, df_str


def merge_dataframes_no_tempo(df: dd.DataFrame, df_str: DataFrame) -> dd.DataFrame:

    # Merge dos dataframes com base no tempo
    df = df.reset_index()
    df = df.merge(df_str, on=cr.DadosVariaveis.TEMPO_UTC0, how="left")

    return df


# FUNÇÔES INTERMEDIÁRIAS -------------------------------------------------------------------------------


def nc_para_dask_dataframe_simples(plataforma: str | None) -> dd.DataFrame:
    """Converte NetCDF em Dask DataFrame, salvando como parquet, preservando variáveis 1D e 2D.
    
    Parâmetros:
    - caminho_dataset_relativo: caminho do dataset em relação à data/datasets/coordenadas_especificas/plataformas ou 
    data/datasets/coordenadas_especificas/ponto_nao_plataforma
    - caminho_dataframe_relativo: caminho da pasta onde ficará o dask dataframe em relação à data/dataframes/coordenadas_especificas/plataformas ou
    data/dataframes/coordenadas_especificas/ponto_nao_plataforma
    Caso nenhum caminho seja passado, será utilizado um caminho correspondente ao do dataset usado.
    """

    dataset_arquivo_caminho = pad.obtem_path_coord_especifica("netcdf", plataforma)
    dataframe_arquivo_caminho = pad.obtem_path_coord_especifica("parquet", plataforma)
    ds = ler_arquivo(fa.NETCDF, dataset_arquivo_caminho, eh_caminho_relativo = False)
    ds = cast(xr.Dataset, ds)

    df, df_str = monta_dataframes_por_dimensao(ds)

    df = merge_dataframes_no_tempo(df, df_str)

    salva_dask_dataframe_parquet(df, dataframe_arquivo_caminho)

    return df



def nc_para_dask_dataframe_todas_plataformas():

    plataformas = Plataformas.PLATAFORMAS # Lista de plataformas
    i = 1

    for plat in plataformas:
        print(f" -> -> -> Plataforma: {plat} ({representa_progresso(i, plataformas)})\n")
        df = nc_para_dask_dataframe_simples(plat)
        i += 1

    print("Todos os dataframes foram salvos!\n")
    
    return df  # Retorna o dataframe da última plataforma


# FUNÇÃO PRINCIPAL -------------------------------------------------------------------------------

def converte_nc_para_dask_dataframe(usa_plataformas: bool = True) -> None:

    print("--- CRIAÇÃO DE DATAFRAME(S) ---\n\n")
    
    if usa_plataformas : 
        nc_para_dask_dataframe_todas_plataformas()

    elif not usa_plataformas:
        nc_para_dask_dataframe_simples(None)



if __name__ == "__main__":
    df = converte_nc_para_dask_dataframe()