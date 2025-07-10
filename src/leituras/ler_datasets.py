from pathlib import Path
import xarray as xr



def ler_dataset_nc(caminho: Path) -> xr.Dataset:
    
    try:
        ds = xr.open_dataset(caminho, engine="netcdf4")
    except OSError as e:
        raise ValueError(f"Erro ao ler o arquivo NetCDF: {e}")


    return ds


