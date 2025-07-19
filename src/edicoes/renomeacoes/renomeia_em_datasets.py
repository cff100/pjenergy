import xarray as xr
from config.constants import Correspondencias as cr

def dataset_renomeacoes(dataset: xr.Dataset) -> xr.Dataset:
    """Renomeia coordenadas/variáveis do dataset.
    
    Args:
        dataset (xr.Dataset): Dataset a ser alterado.

    Returns:
        xr.Dataset: Dataset com renomeações.
    """
   

    dicionario_renomear = cr.DadosVariaveis.NOVOS_NOMES
    ds = dataset.rename(dicionario_renomear)

    return ds