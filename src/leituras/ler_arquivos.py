from pathlib import Path
import xarray as xr
from typing import Literal
import dask.dataframe as dd

from utils.existencia_path import verifica_erro_nao_existe_path
from config.paths import PathsDados
from leituras.ler_datasets import ler_dataset_nc
from leituras.ler_dataframes import ler_dataframe_parquet
from config.constants import FormatosArquivo as fa



def identifica_caminho_base(formato_arquivo: str) -> Path:
    """Identifica o caminho base da pasta de dados de acordo com o tipo de arquivo desejado"""

    if formato_arquivo not in fa.FORMATOS_ACEITOS:
        raise ValueError(f"Formato... \n-> {formato_arquivo} \n...não aceito.")
    elif formato_arquivo == fa.NETCDF:
        caminho_base = PathsDados.Datasets.BASE
    elif formato_arquivo == fa.PARQUET:
        caminho_base = PathsDados.Dataframes.BASE

    return caminho_base



def ler_arquivo(formato_arquivo: Literal["netcdf", "parquet"],
                path: Path | str, 
                eh_caminho_relativo: bool = True, 
                caminho_base: Path | Literal["padrao"] = "padrao") -> xr.Dataset | dd.DataFrame:
    """Lê um arquivo de acordo com o tipo de arquivo e o path fornecido.

    Parâmetros:
    - path: Caminho do arquivo a ser lido. Pode ser um Path ou uma string. 
    No caso de dask dataframes, o caminho deve ser de uma pasta onde os arquivos estão armazenados. 
    Mas também pode ser passado o caminho de um arquivo parquet específico, que será lido como um dataframe.
    - formato_arquivo: Formato do arquivo a ser lido. Pode ser "netcdf", "parquet".
    - eh_caminho_relativo: Se o caminho é relativo ao caminho base. Se for True, o caminho será concatenado com o caminho base.
    - caminho_base: Caminho base a ser usado caso o caminho seja relativo. Se for "padrao", o caminho base será identificado de acordo com o formato do arquivo. Se for passado um caminho, ele será usado como caminho base.
    
    Retorna:
    - Um xr.Dataset se o formato for "netcdf", ou um dd.DataFrame se o formato for "parquet".
    """

    # Para manter em um formato padrão (path) para as próximas funções
    if isinstance(path, str):
        path = Path(path)

    # Caso o caminho seja relativo, pega o caminho base padrão que varia de acordo com o tipo de arquivo
    if eh_caminho_relativo and caminho_base == "padrao":
        caminho_base = identifica_caminho_base(formato_arquivo)

    # Verifica se o caminho passado é relativo a um caminho base (que também é um parâmetro)
    if eh_caminho_relativo:
        path = caminho_base / path

    # Verifica a existência do caminho
    verifica_erro_nao_existe_path(path)


    if formato_arquivo == fa.NETCDF:
        d = ler_dataset_nc(path)
    elif formato_arquivo == fa.PARQUET:
        d = ler_dataframe_parquet(path)

    return d



if __name__ == "__main__":
    #d = ler_arquivo("netcdf", "unido/dataset_unido.nc")
    d = ler_arquivo("parquet", "coordenadas_especificas/plataformas/p1-NAMORADO_2_(PNA-2)")
    print(d.compute())

