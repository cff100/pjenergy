import xarray as xr
from typing import cast
from pathlib import Path
import dask.dataframe as dd
from pandas import DataFrame
from typing import Literal
from leituras.ler_arquivos import ler_arquivo
from config.paths import PathsDados as pad
from config.constants import FormatosArquivo as fa, Correspondencias as cr, Plataformas
from salvamentos.salva_dataframes import salva_dask_dataframe_parquet
from utils.verifica_argumentos_padrao import erro_algum_parametro_diferente_do_padrao, erro_algum_parametro_igual_ao_padrao


# FUNÇÔES AUXILIARES -------------------------------------------------------------------------------

def decide_caminhos_base(localizacao_tipo: Literal["plataforma", "outra_localizacao"]) -> tuple[Path, Path]:

    if localizacao_tipo == "plataforma":
        dataset_caminho_base = pad.Datasets.DIRETORIO_PLATAFORMAS
        dataframe_caminho_base = pad.Dataframes.DIRETORIO_PLATAFORMAS
    elif localizacao_tipo == "outra_localizacao":
        dataset_caminho_base = pad.Datasets.DIRETORIO_NAO_PLATAFORMAS
        dataframe_caminho_base = pad.Dataframes.DIRETORIO_NAO_PLATAFORMAS

    return dataset_caminho_base, dataframe_caminho_base

def monta_dataframes_por_dimensao(ds: xr.Dataset) -> tuple[dd.DataFrame, DataFrame]:

    # Seleciona variáveis 2D (tempo e altura) e monta um dataframe com elas
    variaveis_2d = [v for v in ds.data_vars if ds[v].dims == (cr.TEMPO_UTC0, cr.ALTURA)]
    ds_2d = ds[variaveis_2d].chunk({cr.TEMPO_UTC0: 200})
    df = ds_2d.to_dask_dataframe()

    # Seleciona variáveis 1D (somente tempo) e monta um dataframe com elas
    variaveis_1d_str = [v for v in ds.data_vars if ds[v].dims == (cr.TEMPO_UTC0,)]
    df_str = ds[variaveis_1d_str].to_dataframe().reset_index()

    return df, df_str


def merge_dataframes_no_tempo(df: dd.DataFrame, df_str: DataFrame) -> dd.DataFrame:

    # Merge dos dataframes com base no tempo
    df = df.reset_index()
    df = df.merge(df_str, on=cr.TEMPO_UTC0, how="left")

    return df

def obtem_dataframe_dataset_nomes(dataset_arquivo_nome: str, dataframe_pasta_nome: str, dataframe_caminho_base: Path) -> Path:

    if dataset_arquivo_nome == "padrao":
        
    if dataframe_pasta_nome == "padrao":
        dataframe_pasta_nome = dataset_arquivo_nome.split(".nc")[0]
    dataframe_diretorio_absoluto = dataframe_caminho_base / dataframe_pasta_nome

    return dataframe_diretorio_absoluto


# FUNÇÔES INTERMEDIÁRIAS -------------------------------------------------------------------------------


def nc_para_dask_dataframe_simples(localizacao_tipo: Literal["plataforma", "outra_localizacao"], 
                                   dataset_arquivo_nome: str = "padrao", 
                                   dataframe_pasta_nome: str = "padrao") -> dd.DataFrame:
    """Converte NetCDF em Dask DataFrame, salvando como parquet, preservando variáveis 1D e 2D.
    
    Parâmetros:
    - caminho_dataset_relativo: caminho do dataset em relação à data/datasets/coordenadas_especificas/plataformas ou 
    data/datasets/coordenadas_especificas/ponto_nao_plataforma
    - caminho_dataframe_relativo: caminho da pasta onde ficará o dask dataframe em relação à data/dataframes/coordenadas_especificas/plataformas ou
    data/dataframes/coordenadas_especificas/ponto_nao_plataforma
    Caso nenhum caminho seja passado, será utilizado um caminho correspondente ao do dataset usado.
    """

    dataset_caminho_base, dataframe_caminho_base = decide_caminhos_base(localizacao_tipo)

    dataframe_diretorio_absoluto = obtem_dataframe_dataset_nomes(dataset_arquivo_nome, dataframe_pasta_nome, dataframe_caminho_base)

    ds = ler_arquivo(fa.NETCDF, dataset_arquivo_nome, eh_caminho_relativo = True, caminho_base = dataset_caminho_base)

    ds = cast(xr.Dataset, ds)


    df, df_str = monta_dataframes_por_dimensao(ds)

    df = merge_dataframes_no_tempo(df, df_str)

    salva_dask_dataframe_parquet(df, dataframe_diretorio_absoluto)

    return df



def nc_para_dask_dataframe_todas_plataformas():

    plataformas = Plataformas.PLATAFORMAS # Lista de plataformas

    i = 1
    n = len(plataformas)

    for plat in plataformas:
        print(f"Plataforma: {plat} ({i}/{n})")
        df = nc_para_dask_dataframe_simples("plataforma", Plataformas.PLATAFORMAS_DADOS[plat][cr.ARQUIVO_NC_CHAVE])
        i += 1

    print("Todos os dataframes foram salvos!")
    
    return df  # Retorna o dataframe da última plataforma


# FUNÇÃO PRINCIPAL -------------------------------------------------------------------------------

def converte_nc_para_dask_dataframe(multiplas_plataformas: bool = True, 
                                    dataset_arquivo_nome: str = "padrao", 
                                    dataframe_pasta_nome: str = "padrao") -> dd.DataFrame:
    
    # Monta lista com parametros que tem a possibilidade de receber o valor 'padrao'
    parametros_possivel_padrao = [dataset_arquivo_nome, dataframe_pasta_nome]

    if multiplas_plataformas :
        erro_algum_parametro_diferente_do_padrao(parametros_possivel_padrao, 
                                                 "Quando 'multiplas_plataformas' é True, se pode usar apenas o valor 'padrao' para os parâmetros.")
        nc_para_dask_dataframe_todas_plataformas()
    elif not multiplas_plataformas:
        erro_algum_parametro_igual_ao_padrao(parametros_possivel_padrao, 
                                             "Quando 'multiplas_plataformas' é False, não se pode usar o valor 'padrao' para nenhum parâmetro.")
    
        nc_para_dask_dataframe_simples("outra_localizacao", dataset_arquivo_nome, dataframe_pasta_nome)

    return df  


if __name__ == "__main__":
    #df = nc_para_dask_dataframe("plataformas/p1-NAMORADO_2_(PNA-2).nc")
    df = nc_para_dask_dataframe_todas_plataformas()