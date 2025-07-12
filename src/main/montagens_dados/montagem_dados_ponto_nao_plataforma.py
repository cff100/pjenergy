from typing import Optional
from geracoes.gera_datasets_editados import gera_datasets_editados_pontuais
from geracoes.gera_dataframes import converte_nc_para_dask_dataframe

def montagem_dados_ponto_nao_plataforma(latitude_longitude_alvo: Optional[tuple[float, float]]) -> None:

    ds = gera_datasets_editados_pontuais(False, latitude_longitude_alvo)

    df = converte_nc_para_dask_dataframe(False, )