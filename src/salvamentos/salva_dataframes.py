from pathlib import Path
import dask.dataframe as dd
from dask.diagnostics.progress import ProgressBar
from utils.existencia_path import garante_path_pai_existencia


def salva_dask_dataframe_parquet(dataframe: dd.DataFrame, dataframe_diretorio: Path) -> None:

    # Garante a existência do diretorio da pasta onde a pasta do dataframe está contida
    garante_path_pai_existencia(dataframe_diretorio)

    with ProgressBar():
        print("Salvando...")
        dataframe.to_parquet(dataframe_diretorio, write_index=True, overwrite=True)
        print("Dataframe salvo com sucesso!")
        print("\n")