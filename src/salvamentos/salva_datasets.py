from pathlib import Path
import xarray as xr
from utils.existencia_path import garante_path_pai_existencia

def salva_dataset_nc(dataset: xr.Dataset, dataset_caminho: Path) -> None:
    """Salva o dataset em um arquivo .nc. 
    """

    # Garante a extensão correta do arquiv e gera um arquivo NetCDF
    if not dataset_caminho.suffix == ".nc":
        raise ValueError("O caminho do dataset não possui a extensão .nc")

    print("Salvando arquivo...\n")

    # Garante que a pasta onde o arquivo será salvo exista
    garante_path_pai_existencia(dataset_caminho)
    
    dataset.to_netcdf(dataset_caminho)

    print(f"Dataset salvo em: {dataset_caminho}\n\n")