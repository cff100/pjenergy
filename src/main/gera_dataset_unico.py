from pathlib import Path
from xarray import Dataset
# Módulos internos do projeto
from datasets_operations.une_nc import concatena_datasets, merge_datasets
from config.paths import DIRETORIO_DATASETS_ORIGINAIS, CAMINHO_ABSOLUTO_DATASET_UNIDO
from datasets_operations.salva_dataset import salva_dataset_nc

def gera_dataset_unico(diretorio: Path = DIRETORIO_DATASETS_ORIGINAIS) -> Dataset:
    """Gera um dataset único a partir dos datasets de combinações de variáveis, anos e níveis de pressão."""

    # Concatena os datasets de níveis de pressão e anos diferentes
    dicio_parametros = concatena_datasets(diretorio)

    # Une os datasets de todas variáveis
    dataset_unico = merge_datasets(dicio_parametros)

    # Salva o dataset em um arquivo NetCDF único
    salva_dataset_nc(dataset_unico, CAMINHO_ABSOLUTO_DATASET_UNIDO)

    return dataset_unico

if __name__ == "__main__":
    # Executa a função para gerar o dataset único
    dataset_unico = gera_dataset_unico()
    print(dataset_unico)
    