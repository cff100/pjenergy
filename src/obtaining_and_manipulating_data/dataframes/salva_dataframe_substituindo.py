from pathlib import Path
import shutil
import dask.dataframe as dd
import os
from config.paths import DIRETORIO_DATAFRAME_TEMPORARIO

def salva_dataframe_substituindo(novo_dataframe: dd.DataFrame, diretorio_a_substituir: Path, diretorio_dataframe_temporario: Path = DIRETORIO_DATAFRAME_TEMPORARIO):

    # Salva o dask dataframe em um diretório temporário
    novo_dataframe.to_parquet(diretorio_dataframe_temporario)

    # Apaga o diretório que será substituído
    shutil.rmtree(diretorio_a_substituir)

    # Renomeia o diretório temporário com o mesmo nome do que foi apagado
    os.rename(diretorio_dataframe_temporario, diretorio_a_substituir)
