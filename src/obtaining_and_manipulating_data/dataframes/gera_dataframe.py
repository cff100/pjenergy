import xarray as xr
from pathlib import Path
import dask.dataframe as dd
# Módulos internos do projeto
from config.paths import CAMINHO_NC_UNICO, DIRETORIO_DATAFRAME_PRIMARIO

def gera_arquivos_parquet(caminho_nc_unico: Path = CAMINHO_NC_UNICO, diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_PRIMARIO) -> dd.DataFrame:
    """Gera arquivos Parquet a partir de um arquivo NetCDF único.
    É utilizado dask pois o dataset é grande e possivelmente não cabe na memória."""

    # Carrega o dataset com dask, sem definir chunks específicos
    ds = xr.open_dataset(caminho_nc_unico, chunks={}) 

    # Unifica os chunks em todas as variáveis nas dimensões em comum
    ds = ds.unify_chunks()

    # Converte o dataset para um DataFrame do Dask
    df = ds.to_dask_dataframe()

    # Salva o DataFrame como um conjunto de arquivos Parquet
    df.to_parquet(diretorio_dados_parquet, write_index=True)

    return df

