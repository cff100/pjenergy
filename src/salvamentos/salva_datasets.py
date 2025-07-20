from pathlib import Path
import xarray as xr
from utils.existencia_path import garante_path_pai_existencia

def salva_dataset_nc(dataset: xr.Dataset, dataset_caminho: Path) -> None:
    """Salva o dataset em um arquivo .nc. 

    Args:
        dataset (xr.Dataset): Dataset a ser salvo.
        dataset_caminho (Path): Caminho absoluto do dataset a ser salvo. 
            As pastas parentais são criadas caso não existam.
    """

    # Garante a extensão correta do arquiv e gera um arquivo NetCDF
    if not dataset_caminho.suffix == ".nc":
        raise ValueError("O caminho do dataset não possui a extensão .nc")

    # Garante que a pasta onde o arquivo será salvo exista
    garante_path_pai_existencia(dataset_caminho)
    
    print("Salvando arquivo...\n")

    dataset.to_netcdf(dataset_caminho)

    print(f"Dataset salvo em: {dataset_caminho}\n\n")