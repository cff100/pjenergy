from pathlib import Path
import xarray as xr
from config.paths import CAMINHO_ABSOLUTO_DATASET_UNIDO


def salva_dataset_nc(dataset: xr.Dataset, caminho_dataset: Path) -> None:
    """Salva o dataset em um arquivo .nc. 
    """
    
    # Garante a extensão correta do arquiv e gera um arquivo NetCDF
    if not caminho_dataset.suffix == ".nc":
        caminho_dataset = caminho_dataset.with_suffix(".nc")
    print("Salvando arquivo...\n")
    dataset.to_netcdf(caminho_dataset)
    print(f"Dataset salvo em: {caminho_dataset}\n\n")