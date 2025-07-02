from pathlib import Path
import dask.dataframe as dd
# Módulos internos do projeto
from config.paths import CAMINHO_NC_UNICO, DIRETORIO_DATAFRAME_PRIMARIO
from obtaining_and_manipulating_data.dataframes.gera_dataframe import gera_arquivos_parquet_dataframe
from obtaining_and_manipulating_data.dataframes.adiciona_colunas_dataframe import adiciona_colunas_novas

def gera_dataframe(caminho_nc_unico: Path = CAMINHO_NC_UNICO, diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_PRIMARIO) -> dd.DataFrame:
    """Gera um DataFrame a partir de um arquivo NetCDF único, criando novas colunas de tempo e velocidade resultante."""

    gera_arquivos_parquet_dataframe(caminho_nc_unico, diretorio_dados_parquet)
    df_novas_colunas = adiciona_colunas_novas()
    
    return df_novas_colunas


if __name__ == "__main__":
    # Executa a função para gerar o DataFrame
    df = gera_dataframe()
    print(df.head(100000))  # Exibe as primeiras linhas do DataFrame gerado