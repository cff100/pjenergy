import xarray as xr
from pathlib import Path
from config.paths import CAMINHO_NC_UNICO, CAMINHO_DADOS_PARQUET

def gera_arquivos_parquet(caminho_nc_unico: Path = CAMINHO_NC_UNICO, caminhos_dados_parquet = CAMINHO_DADOS_PARQUET):
    """Gera arquivos Parquet a partir de um arquivo NetCDF único.
    É utilizado dask pois o dataset é grande e possivelmente não cabe na memória."""

    ds = xr.open_dataset(caminho_nc_unico, chunks={})

    # Unifica os chunks em todas as variáveis nas dimensões em comum
    ds = ds.unify_chunks()

    df = ds.to_dask_dataframe()

    df.to_parquet(caminhos_dados_parquet, write_index=True)

    return df

# if __name__ == "__main__":
#     #df = gera_arquivos_parquet()

#     # import dask.dataframe as dd 
#     # import pandas as pd

#     # df = dd.read_parquet(CAMINHO_DADOS_PARQUET)
#     # pd.set_option('display.max_columns', None)  # Mostra todas as colunas
#     # # Ajustar largura para caber melhor no terminal
#     # pd.set_option('display.width', 0)           # Quebra de linha automática no terminal
#     # print(df.head(2))
#     # print(df.tail(2))