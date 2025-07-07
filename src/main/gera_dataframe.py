# from pathlib import Path
# import dask.dataframe as dd
# # Módulos internos do projeto
# from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO, DIRETORIO_DATAFRAME_PRIMARIO
# from datasets_operations.dataframes.gera_dataframe import nc_para_dataframe
# from datasets_operations.dataframes.edita_dataframe import edita_colunas

# def gera_dataframe(caminho_nc_unico: Path = CAMINHO_RELATIVO_DATASET_UNIDO, diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_PRIMARIO) -> dd.DataFrame:
#     """Gera um DataFrame a partir de um arquivo NetCDF único e faz edições nas colunas."""

#     nc_para_dataframe(caminho_nc_unico, diretorio_dados_parquet)
#     df_editado = edita_colunas()
    
#     return df_editado


# if __name__ == "__main__":
#     # Executa a função para gerar o DataFrame
#     df = gera_dataframe()
#     print(df.head(100000))  # Exibe as primeiras linhas do DataFrame gerado