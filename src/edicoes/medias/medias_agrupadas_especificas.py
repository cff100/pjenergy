import dask.dataframe as dd
from typing import Optional

from edicoes.medias.media_agrupada import media_agrupada

def media_mensal(plataforma_representacao: Optional[str] = None, 
                         df: Optional[dd.DataFrame] = None) -> dd.DataFrame:
    """
    Faz a média agrupada por mês e altura.
    """
    
    categoria_de_agrupamento: list = ["mes_nome", "h"]
    colunas_remover = ["dia", "hora_str", "tempo_bras", "data_bras", "hora", "estacao"]

    media = media_agrupada(categoria_de_agrupamento, colunas_remover, plataforma_representacao, df)

    return media


if __name__ == "__main__":

    media = media_mensal(plataforma_representacao = "p7")
    print(media.compute().head(50))
    print(media[media["ano"] == 2023].compute())