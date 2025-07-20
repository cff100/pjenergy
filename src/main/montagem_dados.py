from typing import Optional
from geracoes.gera_datasets_editados import gera_datasets_editados_pontuais
from geracoes.gera_dataframes import converte_nc_para_dask_dataframe

def montagem_dados(usa_plataformas: bool = True, 
                                        latitude_longitude_alvo: Optional[tuple[float, float]] = None) -> None:
    """Monta datasets editados para localizações específicas a partir dos datasets obtidos do CDS e 
    depois cria dataframes a partir destes datasets editados
    
    Args: 
        usa_plataformas: Se True, gera dados para todas plataformas. Se False, gera dados para as coordenadas fornecidas.
        latitude_longitude_alvo (Optional[tuple[float, float]]): Coordenadas caso não seja escolhida uma plataforma.
    """

    gera_datasets_editados_pontuais(usa_plataformas, latitude_longitude_alvo)

    converte_nc_para_dask_dataframe(usa_plataformas)


if __name__ == "__main__":
    montagem_dados()