import xarray as xr
from pathlib import Path
from datasets_operations.edita_dataset import cria_dataset_ponto_especifico
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO


def gera_dataset_editado(plataforma: str | None = None, latitude_longitude_alvo: tuple[float, float] | None = None, caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> xr.Dataset:
    "Gera a forma final do dataset único"
    
    ds = cria_dataset_ponto_especifico(plataforma, latitude_longitude_alvo, caminho_relativo_dataset_unico)
    return ds

if __name__ == "__main__":
    ds = gera_dataset_editado()
    print(ds)