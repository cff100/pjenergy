import xarray as xr
from datasets_operations.edita_dataset import edita_dataset_unico

def gera_dataset_editado() -> xr.Dataset:
    "Gera a forma final do dataset único"
    ds = edita_dataset_unico()
    return ds

if __name__ == "__main__":
    ds = gera_dataset_editado()
    print(ds)