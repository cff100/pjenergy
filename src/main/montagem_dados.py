from typing import Optional
from geracoes.gera_datasets_editados import gera_datasets_editados_pontuais

def montagem_dados(usa_plataformas: bool = True, 
                    latitude_longitude_alvo: Optional[tuple[float, float]] = None):


    ds = gera_datasets_editados_pontuais(usa_plataformas, latitude_longitude_alvo)