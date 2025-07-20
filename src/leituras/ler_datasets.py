from pathlib import Path
import xarray as xr



def ler_dataset_nc(caminho: Path) -> xr.Dataset:
    """Lê dataset no formato NetCDF.
    
    Args:
        diretorio (Path): Diretório do dataset

    Returns:
        dd.Dataset: Dataset lido.

    Raises:
        ValueError: Erro de leitura do dataset.
    """
    
    try:
        ds = xr.open_dataset(caminho, engine="netcdf4")
    except OSError as e:
        raise ValueError(f"Erro ao ler o arquivo NetCDF: {e}")


    return ds


