import xarray as xr
from pathlib import Path
from datasets_operations.edita_dataset import edita_dataset_unico
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO, CAMINHO_ABSOLUTO_DATASET_EDITADO


def gera_dataset_editado(lat_long_alvo: tuple[float, float], caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO, 
                        caminho_absoluto_dataset_editado: Path = CAMINHO_ABSOLUTO_DATASET_EDITADO) -> xr.Dataset:
    "Gera a forma final do dataset único"
    
    ds = edita_dataset_unico(lat_long_alvo, caminho_relativo_dataset_unico, caminho_absoluto_dataset_editado)
    return ds

if __name__ == "__main__":
    ds = gera_dataset_editado((-22.0, -40.0))
    print(ds)