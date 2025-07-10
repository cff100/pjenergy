import xarray as xr
from pathlib import Path
from dask.diagnostics.progress import ProgressBar
import dask.dataframe as dd
# Módulos internos do projeto
from leituras.ler_arquivos import ler_arquivo
from config.paths import decide_caminho_absoluto_dataset_localizacao_especifica, caminho_absoluto_dataframe_plataforma
from utils.gerencia_plataformas_representacoes import gerencia_plataforma_nome
from config.constants import OutrasConstantes as oc, FormatosArquivo as fa, Correspondencias as cr


def nc_para_dask_dataframe(caminho_dataset: Path, caminho_dataframe: Path) -> dd.DataFrame:
    """Converte NetCDF em Dask DataFrame, salvando como parquet, preservando variáveis 1D e 2D."""

    ds = ler_arquivo(caminho_dataset, formato_arquivo = fa.NETCDF, eh_caminho_relativo = False)

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

    # Salvar como parquet
    with ProgressBar():
        print("Salvando dataframe gerado...")
        df.to_parquet(caminho_dataframe, write_index=True, overwrite=True)
        print("\n")

    return df


def plataforma_nc_para_dataframe_ponto_especifico(plataforma: str | None = None) -> dd.DataFrame:
    """Gera um dataframe a partir de um arquivo NetCDF das plataformas."""

    if plataforma:
        plataforma = gerencia_plataforma_nome(plataforma)
    
    caminho_absoluto_dataset = decide_caminho_absoluto_dataset_localizacao_especifica(plataforma)
    caminho_absoluto_dataframe = caminho_absoluto_dataframe_plataforma(plataforma)

    df = nc_para_dask_dataframe(caminho_absoluto_dataset, caminho_absoluto_dataframe)

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