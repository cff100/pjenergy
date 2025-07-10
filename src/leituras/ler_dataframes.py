from pathlib import Path
import dask.dataframe as dd



def ler_dataframe_parquet(caminho: Path) -> dd.DataFrame:
    
    try:
        df = dd.read_parquet(caminho)
    except OSError as e:
        raise ValueError(f"Erro ao ler o dataframe: {e}")


    return df