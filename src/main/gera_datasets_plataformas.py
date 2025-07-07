from pathlib import Path
from datasets_operations.edita_dataset import cria_datasets_plataformas
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO


def gera_datasets_plataformas(caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> None:
    "Gera a forma datasets para os pontos de todas as plataformas com dados de uma lista de alturas específicas."
    
    cria_datasets_plataformas(caminho_relativo_dataset_unico)


if __name__ == "__main__":
    gera_datasets_plataformas()
