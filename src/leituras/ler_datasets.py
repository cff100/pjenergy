from pathlib import Path
import xarray as xr



def ler_dataset_nc(caminho: Path) -> xr.Dataset:
    
    try:
        ds = xr.open_dataset(caminho, engine="netcdf4")
    except FileNotFoundError:
        raise ValueError(f"Caminho... \n -> {caminho} \n...não encontrado")


    return ds


