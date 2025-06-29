import xarray as xr
from pathlib import Path
# Módulos internos do projeto
from config.paths import CAMINHO_DADOS_NC, CAMINHO_TESTES_ARQUIVOS_NOVOS
from utils.cria_caminho_arquivo import cria_caminho_arquivo


def ler_nc_infomacoes_principais(arquivo_nc_caminho_relativo: Path | str, caminho_base: Path = CAMINHO_DADOS_NC) -> xr.Dataset:
    """Lê um arquivo .nc e retorna as informações principais do dataset."""
    """Parâmetros:
    arquivo_nc_caminho_relativo: Caminho relativo do arquivo .nc em relação ao caminho base. 
    Pode também ser uma string porque quando composto com o caminho base, ele se torna um Path.
    """

    arquivo_nc_caminho = cria_caminho_arquivo(arquivo_nc_caminho_relativo, caminho_base)

    # Verifica se o arquivo existe
    if not arquivo_nc_caminho.exists():
        raise FileNotFoundError(f"O arquivo {arquivo_nc_caminho} não foi encontrado.")
    ds = xr.open_dataset(arquivo_nc_caminho, engine="netcdf4")
    return ds


if __name__ == "__main__":
    #ds_1 = ler_nc_infomacoes_principais("(var-temperature)_(anos-2015)_(pressao-950).nc")
    #print("ds_1: \n", ds_1)
    #print(ds_1.valid_time)
    #print(ds_1.expver[0])

    #ds_2 = ler_nc_infomacoes_principais("(var-geopotential)_(anos-2020)_(pressao-925).nc", CAMINHO_TESTES_ARQUIVOS_NOVOS)
    #print("\n\n\n ds_2: \n", ds_2)

    ds_3 = ler_nc_infomacoes_principais("dataset_unico.nc")
    print(ds_3)