import xarray as xr
from pathlib import Path
from dask.diagnostics.progress import ProgressBar
import dask.dataframe as dd
# Módulos internos do projeto
from datasets_operations.ler_nc import ler_dataset_nc_absoluto
from config.paths import caminho_absoluto_dataset_plataforma, caminho_absoluto_dataframe_plataforma
from utils.gerencia_plataforma_nome import gerencia_plataforma_nome
from config.constants import OutrasConstantes as oc, NomeColunasDataframe as ncd


def nc_para_dataframe(caminho_absoluto_dataset: Path, caminho_absoluto_dataframe: Path) -> dd.DataFrame:
    """Converte NetCDF em Dask DataFrame, salvando como parquet, preservando variáveis 1D e 2D."""

    ds = ler_dataset_nc_absoluto(caminho_absoluto_dataset)

    # for var in ds.data_vars:
    #     print(f"{var}: {ds[var].dims}")
    assert isinstance(ncd.tempo_UTC0, str)
    # Seleciona variáveis 2D (tempo e altura)
    variaveis_2d = [v for v in ds.data_vars if ds[v].dims == ('tempo_UTC0', 'altura')]
    # print(variaveis_2d)

    ds_2d = ds[variaveis_2d].chunk({ncd.tempo_UTC0: 200})

    df = ds_2d.to_dask_dataframe()

    # Seleciona variáveis 1D (somente tempo)
    variaveis_1d_str = [v for v in ds.data_vars if ds[v].dims == (ncd.tempo_UTC0,)]
    # print(variaveis_1d_str)
    df_str = ds[variaveis_1d_str].to_dataframe().reset_index()

    # Merge com base no tempo
    df = df.reset_index()
    df = df.merge(df_str, on=ncd.tempo_UTC0, how="left")

    # Salvar como parquet
    with ProgressBar():
        print("Salvando dataframe gerado...")
        df.to_parquet(caminho_absoluto_dataframe, write_index=True, overwrite=True)
        print("\n")

    return df


def plataforma_nc_para_dataframe_ponto_especifico(plataforma: str | None = None) -> dd.DataFrame:
    """Gera um dataframe a partir de um arquivo NetCDF das plataformas."""

    if plataforma:
        plataforma = gerencia_plataforma_nome(plataforma)
    
    caminho_absoluto_dataset = caminho_absoluto_dataset_plataforma(plataforma)
    caminho_absoluto_dataframe = caminho_absoluto_dataframe_plataforma(plataforma)

    df = nc_para_dataframe(caminho_absoluto_dataset, caminho_absoluto_dataframe)

    return df

    
def converte_nc_para_dataframes_ponto_especifico(alternativa_plataforma: str | None = None) -> dd.DataFrame | None:

    """Decide o modo de chamar a função de geração de dataframe dependendo da escolha de todas as plataformas (alternativa_plataforma = 'all') ou 
    um ponto específico (alternativa_plataforma = None)"""
    
    if alternativa_plataforma == "all":
        for plat in list(oc.plataformas_dados.keys()):
            print(f"Plataforma: {plat}")
            df = plataforma_nc_para_dataframe_ponto_especifico(plat)
            return df

    elif alternativa_plataforma is None:
        df = plataforma_nc_para_dataframe_ponto_especifico()
        return df
    


if __name__ == "__main__":
    df = converte_nc_para_dataframes_ponto_especifico()
    if df is not None:
        print(df)