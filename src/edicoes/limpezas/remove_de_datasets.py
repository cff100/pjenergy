import xarray as xr
from config.constants import Correspondencias as cr

def remove_variaveis_indesejadas(dataset:xr.Dataset) -> xr.Dataset:
    "Remove coordenadas e variáveis indesejadas."

    lista_remover = [cr.NUMBER, cr.EXP_VER]
    ds = dataset.drop_vars(lista_remover)

    return ds