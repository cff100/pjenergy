from pathlib import Path
import xarray as xr
# Módulos internos do projeto
from datasets_operations.une_nc import unifica_datasets
from config.paths import DIRETORIO_DATASETS_ORIGINAIS, CAMINHO_ABSOLUTO_DATASET_UNIDO


def gera_dataset_unico(diretorio_datasets_originais: Path = DIRETORIO_DATASETS_ORIGINAIS, 
                     diretorio_dataset_unido: Path = CAMINHO_ABSOLUTO_DATASET_UNIDO) -> xr.Dataset:
    """Gera um dataset único a partir dos datasets de combinações de variáveis, anos e níveis de pressão."""

    dataset_unico = unifica_datasets(diretorio_datasets_originais, diretorio_dataset_unido)

    return dataset_unico

if __name__ == "__main__":
    # Executa a função para gerar o dataset único
    dataset_unico = gera_dataset_unico()
    print(dataset_unico)
    