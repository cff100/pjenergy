from typing import Optional
import xarray as xr
from config.constants import Plataformas
from leituras.ler_arquivos import ler_arquivo
from config.paths import PathsDados as pad
from salvamentos.salva_datasets import salva_dataset_nc
from edicoes.limpezas.remove_de_datasets import remove_variaveis_indesejadas
from edicoes.interpolacoes.interpola_em_datasets import dataset_interpola_lat_lon, interp_alturas_constantes
from edicoes.adicoes.adiciona_a_datasets import adiciona_variaveis
from edicoes.renomeacoes.renomeia_em_datasets import dataset_renomeacoes
from edicoes.unioes.une_nc import unifica_datasets
from utils.representa_progresso import representa_progresso



def processa_edicoes(plataforma: str | None = None, 
                    latitude_longitude_alvo: tuple[float, float] | None = None) -> xr.Dataset:
    "Chama as várias funções que realizam edições sequenciais no dataset único para criar um dataset para uma coordenada específica."

    print("Editando...\n")
    
    # Lê dataset (verificando se o dataset existe)
    ds = ler_arquivo("netcdf", pad.Datasets.CAMINHO_UNIDO, False)

    if not isinstance(ds, xr.Dataset):
        raise TypeError("ds precisa ser um dataset")

    

    processos = [remove_variaveis_indesejadas, dataset_interpola_lat_lon, interp_alturas_constantes, adiciona_variaveis, dataset_renomeacoes]

    for funcao in processos:
        if funcao == dataset_interpola_lat_lon:
            ds = funcao(ds, latitude_longitude_alvo)
        else:
            ds = funcao(ds)

    print("Editado.\n")
    salva_dataset_nc(ds, pad.obter_path_coord_especifica("netcdf", plataforma))

    return ds



def gera_datasets_editados_pontuais(usa_plataformas: bool = True, 
                        latitude_longitude_alvo: Optional[tuple[float, float]] = None) -> xr.Dataset :
    """Gera datasets editados em relação ao dataset unido de ponto geográficos específicos.
    
    Parâmetros:
    - usa_plataformas: Se True, gera datasets para todas plataformas. Se False, gera um dataset para as coordenadas fornecidas."""

    unifica_datasets()

    print("--- EDIÇÃO DE DATASET(S) ---\n\n")

    if usa_plataformas:
        if latitude_longitude_alvo is not None:
            print("\nAVISO: As plataformas já possuem coordenadas registradas, não é necessário passar valores de latitude e longitude.\n")

        plataformas_dados = Plataformas.PLATAFORMAS_DADOS
        i = 1

        for plat in Plataformas.PLATAFORMAS:
            print(f"Plataforma: {plat} ({representa_progresso(i, Plataformas.PLATAFORMAS)})\n")
            latitude_longitude_alvo = plataformas_dados[plat]["coords"]
            ds = processa_edicoes(plat, latitude_longitude_alvo)  # Retorna o valor da última plataforma
            i += 1
    else:
        if latitude_longitude_alvo is None:
            raise ValueError("É necessário informar a latitude e longitude alvo.")
        ds = processa_edicoes(latitude_longitude_alvo = latitude_longitude_alvo)

    return ds 


if __name__ == "__main__":
    ds = gera_datasets_editados_pontuais(False, (-22, -40))
    print(ds)