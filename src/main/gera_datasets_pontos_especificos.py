from pathlib import Path
import xarray as xr
from datasets_operations.edita_dataset import cria_datasets_especificos_alternativas
from config.paths import CAMINHO_RELATIVO_DATASET_UNIDO


def gera_datasets_pontos_especificos(alternativa_plataforma: str | None = None, 
                            latitude_longitude_alvo: tuple[float, float] | None = None, 
                            caminho_relativo_dataset_unico: Path | str = CAMINHO_RELATIVO_DATASET_UNIDO) -> xr.Dataset | None :
    """Gera datasets para os pontos de todas as plataformas ou para um ponto específico com dados de uma lista de alturas específicas."""
    
    ds = cria_datasets_especificos_alternativas(alternativa_plataforma = alternativa_plataforma, 
                                           latitude_longitude_alvo = latitude_longitude_alvo, 
                                           caminho_relativo_dataset_unico = caminho_relativo_dataset_unico)

    return ds


if __name__ == "__main__":
    # Gerar todas as plataformas
    gera_datasets_pontos_especificos(alternativa_plataforma = "all")

    # # Gerar um ponto específico
    ds = gera_datasets_pontos_especificos(latitude_longitude_alvo = (-22, -40))
    print(ds)