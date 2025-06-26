import xarray as xr
from config.paths import CAMINHO_BASE
import os

def caminho_arquivo_nc(arquivo_nc_caminho_relativo):

    arquivo_nc = CAMINHO_BASE / arquivo_nc_caminho_relativo
    return arquivo_nc

def ler_nc_infomacoes_principais(arquivo_nc_caminho_relativo):

    arquivo_nc = caminho_arquivo_nc(arquivo_nc_caminho_relativo)

    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_nc):
        raise FileNotFoundError(f"O arquivo {arquivo_nc} não foi encontrado.")
    ds = xr.open_dataset(arquivo_nc, engine="netcdf4")
    return ds
