import xarray as xr
from config.paths import CAMINHO_DADOS_NC
import os

def caminho_arquivo_nc(arquivo_nc_caminho_relativo, caminho_base = CAMINHO_DADOS_NC):

    arquivo_nc = caminho_base / arquivo_nc_caminho_relativo
    return arquivo_nc

def ler_nc_infomacoes_principais(arquivo_nc_caminho_relativo, caminho_base = CAMINHO_DADOS_NC):

    arquivo_nc = caminho_arquivo_nc(arquivo_nc_caminho_relativo, caminho_base)

    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_nc):
        raise FileNotFoundError(f"O arquivo {arquivo_nc} não foi encontrado.")
    ds = xr.open_dataset(arquivo_nc, engine="netcdf4")
    return ds


if __name__ == "__main__":
    ds = ler_nc_infomacoes_principais("(var-u_component_of_wind)_(anos-2015)_(pressao-950).nc")
    print(ds)