from pathlib import Path
from xarray import Dataset
# Módulos internos do projeto
from obtaining_and_manipulating_data.une_nc import concatena_datasets, merge_datasets, salva_dataset_unico
from config.paths import CAMINHO_DADOS_NC

def gera_dataset_unico(diretorio: Path = CAMINHO_DADOS_NC) -> Dataset:
    """Gera um dataset único a partir dos datasets de combinações de variáveis, anos e níveis de pressão."""

    dicio_parametros = concatena_datasets(diretorio)
    dataset_unico = merge_datasets(dicio_parametros)
    salva_dataset_unico(dataset_unico)

    return dataset_unico

if __name__ == "__main__":
    # Executa a função para gerar o dataset único
    dataset_unico = gera_dataset_unico()
    print(dataset_unico)
    