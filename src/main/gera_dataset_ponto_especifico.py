import xarray as xr
from pathlib import Path
from datasets_operations.edita_dataset import cria_dataset_ponto_especifico
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO


def gera_dataset_editado(latitude_longitude_alvo: tuple[float, float] | None = None, caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> xr.Dataset:
    """Gera um dataset para um ponto específico com dados de uma lista de alturas específicas."""
    
    ds = cria_dataset_ponto_especifico(latitude_longitude_alvo=latitude_longitude_alvo, caminho_relativo_dataset_unico=caminho_relativo_dataset_unico)
    return ds

if __name__ == "__main__":
    # Exemplo
    ds = gera_dataset_editado((-22, -40))
    print(ds)