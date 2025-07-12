import xarray as xr
from pathlib import Path
from dask.diagnostics.progress import ProgressBar
import dask.dataframe as dd
from typing import Optional
# Módulos internos do projeto
from leituras.ler_arquivos import ler_arquivo
from config.paths import PathsDados as pdd
from config.constants import FormatosArquivo as fa, Correspondencias as cr, Plataformas, PastasNomes as pn


def nc_para_dask_dataframe(caminho_dataset_relativo: str , caminho_dataframe_relativo: Optional[str] = None) -> dd.DataFrame:
    """Converte NetCDF em Dask DataFrame, salvando como parquet, preservando variáveis 1D e 2D.
    
    Parâmetros:
    - caminho_dataset_relativo: caminho do dataset em relação à data/datasets/coordenadas_especificas
    - caminho_dataframe_relativo: caminho da pasta onde ficará o dask dataframe em relação à data/dataframes/coordenadas_especificas. 
    Caso nenhum caminho seja passado, será utilizado um caminho correspondente ao do dataset usado.
    """

    ds = ler_arquivo(fa.NETCDF, caminho_dataset_relativo, eh_caminho_relativo = True, caminho_base = pdd.Datasets.DIRETORIO_COORDENADAS_ESPECIFICAS)

    if not isinstance(ds, xr.Dataset):
        raise TypeError("'ds' não é um dataset.")

    # Seleciona variáveis 2D (tempo e altura) e monta um dataframe com elas
    variaveis_2d = [v for v in ds.data_vars if ds[v].dims == ('tempo_UTC0', 'altura')]
    ds_2d = ds[variaveis_2d].chunk({cr.TEMPO_UTC0: 200})
    df = ds_2d.to_dask_dataframe()

    # Seleciona variáveis 1D (somente tempo) e monta um dataframe com elas
    variaveis_1d_str = [v for v in ds.data_vars if ds[v].dims == (cr.TEMPO_UTC0,)]
    df_str = ds[variaveis_1d_str].to_dataframe().reset_index()

    # Merge dos dataframes com base no tempo
    df = df.reset_index()
    df = df.merge(df_str, on=cr.TEMPO_UTC0, how="left")

    if caminho_dataframe_relativo == None:
        caminho_dataframe_relativo = caminho_dataset_relativo.split(".nc")[0]
    caminho_dataframe_absoluto = pdd.Dataframes.DIRETORIO_COORDENADAS_ESPECIFICAS / caminho_dataframe_relativo

    # Salvar como parquet
    with ProgressBar():
        print("Salvando dataframe gerado...")
        df.to_parquet(caminho_dataframe_absoluto, write_index=True, overwrite=True)
        print("Dataframe salvo com sucesso!")
        print("\n")

    return df


def nc_para_dask_dataframe_todas_plataformas():

    plataformas = Plataformas.PLATAFORMAS

    i = 1
    n = len(plataformas)
    for plat in plataformas:
        print(f"Plataforma: {plat} ({i}/{n})")
        caminho_dataset_relativo = pn.PLATAFORMAS + "/" + Plataformas.PLATAFORMAS_DADOS[plat][cr.ARQUIVO_NC_CHAVE] 
        df = nc_para_dask_dataframe(caminho_dataset_relativo)
        i += 1

    print("Todos os dataframes foram salvos!")
    
    return df  # Retorna o dataframe da última plataforma


if __name__ == "__main__":
    #df = nc_para_dask_dataframe("plataformas/p1-NAMORADO_2_(PNA-2).nc")
    df = nc_para_dask_dataframe_todas_plataformas()