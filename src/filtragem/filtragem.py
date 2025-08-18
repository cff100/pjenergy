from pathlib import Path
from typing import Union
import dask.dataframe as dd

def filtra_estacao(dataframe_diretorio_relativo: Union[str, Path], estacoes: Union[str, list]) -> dd.DataFrame:
    """Filtra um dataframe por uma estação ou lista de estações.
    
    Args:
        dataframe_diretorio_relativo (str | Path): Diretório relativo onde está o dataframe. É relativo à "data/dataframes".

        estacoes (str | list): Estação ou lista de estações pelas quais se deseja filtrar.
    """

    pass