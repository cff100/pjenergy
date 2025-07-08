import xarray as xr
from pathlib import Path
# Módulos internos do projeto
from config.paths import DIRETORIO_DATASETS
from utils.cria_caminho_arquivo import cria_caminho_arquivo_relativo


def ler_dataset_nc_relativo(arquivo_nc_caminho_relativo: Path | str, diretorio_base: Path = DIRETORIO_DATASETS) -> xr.Dataset:
    """Lê um arquivo .nc e retorna as informações principais do dataset.
    Parâmetros:
    arquivo_nc_caminho_relativo: Caminho relativo do arquivo .nc em relação ao diretório base. 
    Pode também ser uma string porque quando composto com o caminho base, ele se torna um Path.
    """

    arquivo_nc_caminho = cria_caminho_arquivo_relativo(arquivo_nc_caminho_relativo, diretorio_base)

    # Verifica se o arquivo existe
    if not arquivo_nc_caminho.exists():
        raise FileNotFoundError(f"O arquivo {arquivo_nc_caminho} não foi encontrado.")
    ds: xr.Dataset = xr.open_dataset(arquivo_nc_caminho, engine="netcdf4")
    return ds


def ler_dataset_nc_absoluto(arquivo_nc_caminho_absoluto: Path) -> xr.Dataset:
    """Lê um arquivo .nc e retorna as informações principais do dataset.
    Parâmetros:
    arquivo_nc_caminho_absoluto: Caminho absoluto do arquivo .nc 
    """

    # Verifica se o arquivo existe
    if not arquivo_nc_caminho_absoluto.exists():
        raise FileNotFoundError(f"O arquivo {arquivo_nc_caminho_absoluto} não foi encontrado.")
    ds: xr.Dataset = xr.open_dataset(arquivo_nc_caminho_absoluto, engine="netcdf4")
    return ds


if __name__ == "__main__":
    # Exemplo
    ds = ler_dataset_nc_relativo("plataforms/ponto_nao_especifico.nc")
    #ds = ler_dataset_nc_relativo("plataforms/p9-VERMELHO_2_(PVM-2).nc")
    #ds = ler_dataset_nc_relativo("merged/dataset_unido.nc")
    print(ds)
    #print(ds["z"].sel())
    #print(ds["z"].min())
    #print(ds["z"].max())
