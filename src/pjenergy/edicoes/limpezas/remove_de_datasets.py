import xarray as xr
from config.constants import Correspondencias as cr

def remove_variaveis_indesejadas(dataset:xr.Dataset) -> xr.Dataset:
    """Remove coordenadas/variáveis indesejadas de um dataset.
    
    Args:
        dataset (xr.Dataset): Dataset a ser alterado.

    Returns:
        xr.Dataset: Dataset com remoções.
    """

    lista_remover = [cr.DadosVariaveis.NUMBER, cr.DadosVariaveis.EXP_VER]
    ds = dataset.drop_vars(lista_remover)

    return ds