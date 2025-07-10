from pathlib import Path
import xarray as xr
from typing import Literal, Optional

from utils.existe_path import existe_path
from utils.eh_arquivo import eh_path_arquivo
from config.paths import PathsDados
from leituras.ler_datasets import ler_dataset_nc
from config.constants import FormatosArquivo
from utils.identifica_formato_arquivo import identifica_formato_arquivo



def identifica_caminho_base(tipo_arquivo: FormatosArquivo) -> Path:
    """Identifica o caminho base da pasta de dados de acordo com o tipo de arquivo desejado"""

    if tipo_arquivo == "netcdf":
        caminho_base = PathsDados.Datasets.BASE
    elif tipo_arquivo == "parquet":
        caminho_base = PathsDados.Dataframes.BASE
    
    return caminho_base



def ler_arquivo(caminho: Path | str, formato_arquivo: Optional[FormatosArquivo] = None, eh_caminho_relativo: bool = False, caminho_base: Path | Literal["padrao"] = "padrao") -> xr.Dataset:
    """Lê um arquivo de acordo com o tipo de arquivo e o caminho fornecido."""

    # Para manter em um formato padrão para as próximas funções
    if isinstance(caminho, str):
        caminho = Path(caminho)

    # Identifica o tipo de arquivo caso nenhum seja passado
    if formato_arquivo == None:
        formato_arquivo = identifica_formato_arquivo(caminho)

    # Pega o caminho padrão dependendo do tipo de arquivo
    if caminho_base == "padrao":
        caminho_base = identifica_caminho_base(formato_arquivo)

    # Verifica se o caminho passado é relativo a um caminho base (que também é um parâmetro)
    if eh_caminho_relativo:
        caminho = caminho_base / caminho

    # Captura o erro do caso em que o caminho não é relativo ao mesmo tempo em que o caminho é um str.
    # elif isinstance(caminho, str):
    #     raise TypeError(f"O caminho... \n -> {caminho} \n...é do tipo str. Precisa ser um objeto do tipo Path.")

    # Verifica a existência do caminho
    existe_path(caminho)

    # Verifica se o caminho é de um arquivo (ao invés de um diretório de pasta)
    eh_path_arquivo(caminho)

    if formato_arquivo == "netcdf":
        d = ler_dataset_nc(caminho)
    elif formato_arquivo == "parquet":
        raise NotImplementedError("Leitura de arquivos Parquet ainda não implementada.")
    else:
        raise ValueError(f"Formato de arquivo inválido: {formato_arquivo}")

    return d

if __name__ == "__main__":
    d = ler_arquivo("merged/dataset_unido.nc", "netcdf", eh_caminho_relativo=True)
    print(d)