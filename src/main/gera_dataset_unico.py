from pathlib import Path
# Módulos internos do projeto
from obtaining_and_manipulating_data.une_nc import concatena_datasets, merge_datasets, salva_dataset_unico
from config.paths import CAMINHO_DADOS_NC

def gera_dataset_unico(diretorio: Path = CAMINHO_DADOS_NC) -> None:
    """Gera um dataset único a partir dos datasets de combinações de variáveis, anos e níveis de pressão."""

    dicio_parametros = concatena_datasets(diretorio)
    dataset_unico = merge_datasets(dicio_parametros)
    print(f"Dataset único gerado com {len(dataset_unico.data_vars)} variáveis e {len(dataset_unico.pressure_level)} níveis de pressão.")
    salva_dataset_unico(dataset_unico)

if __name__ == "__main__":
    # Executa a função para gerar o dataset único
    gera_dataset_unico()
    print("Dataset único gerado com sucesso!")