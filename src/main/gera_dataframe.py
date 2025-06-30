from pathlib import Path
import dask.dataframe as dd
# Módulos internos do projeto
from config.paths import CAMINHO_NC_UNICO, CAMINHO_DADOS_PARQUET
from obtaining_and_manipulating_data.dataframes.gera_arquivos_parquet import gera_arquivos_parquet

def gera_dataframe(caminho_nc_unico: Path = CAMINHO_NC_UNICO, diretorio_dados_parquet: Path = CAMINHO_DADOS_PARQUET) -> dd.DataFrame:
    """Gera um DataFrame a partir de um arquivo NetCDF único."""

    df = gera_arquivos_parquet(caminho_nc_unico, diretorio_dados_parquet)
    return df


if __name__ == "__main__":
    # Executa a função para gerar o DataFrame
    df = gera_dataframe()
    print(df.head())  # Exibe as primeiras linhas do DataFrame gerado