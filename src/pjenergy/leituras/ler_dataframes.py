from pathlib import Path
import dask.dataframe as dd

def ler_dataframe_parquet(diretorio: Path) -> dd.DataFrame:
    """Lê dask dataframes no formato parquet.
    
    Args:
        diretorio (Path): Diretório do dask dataframe.

    Returns:
        dd.Dataframe: Dataframe lido.

    Raises:
        ValueError: Erro de leitura do dataframe.
    """
    
    try:
        df = dd.read_parquet(diretorio)
    except OSError as e:
        raise ValueError(f"Erro ao ler o dataframe: {e}")


    return df