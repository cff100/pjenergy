import xarray as xr
from config.constants import Correspondencias as cr

def dataset_renomeacoes(dataset: xr.Dataset) -> xr.Dataset:
    "Renomeia coordenadas/variáveis do dataset."

    dicionario_renomear = cr.DadosVariaveis.NOVOS_NOMES
    ds = dataset.rename(dicionario_renomear)

    return ds