import xarray as xr
from pathlib import Path
from pandas import DataFrame
from dask.diagnostics.progress import ProgressBar
# Módulos internos do projeto
from datasets_operations.ler_nc import ler_dataset_nc
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO, caminho_absoluto_dataframe_plataforma
from utils.gerencia_plataforma_nome import gerencia_plataforma_nome

def nc_para_dataframe(plataforma: str | None = None, caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> DataFrame:
    """Gera um dataframe a partir de um arquivo NetCDF."""

    if plataforma:
        plataforma = gerencia_plataforma_nome(plataforma)
    

    # Lê dataset (verificando se o dataset existe)
    ds = ler_dataset_nc(caminho_relativo_dataset_unico)

    # Gera o dataframe
    df = ds.to_dataframe().reset_index()

    # Salva em um arquivo parquet
    df.to_parquet(caminho_absoluto_dataframe_plataforma(plataforma), index=False)

    return df
    

