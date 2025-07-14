from typing import Optional
from geracoes.gera_datasets_editados import gera_datasets_editados_pontuais
from geracoes.gera_dataframes import converte_nc_para_dask_dataframe

def montagem_dados_ponto_nao_plataforma(usa_plataformas: bool = True, 
                                        latitude_longitude_alvo: Optional[tuple[float, float]] = None) -> None:

    ds = gera_datasets_editados_pontuais(usa_plataformas, latitude_longitude_alvo)

    df = converte_nc_para_dask_dataframe(usa_plataformas, )