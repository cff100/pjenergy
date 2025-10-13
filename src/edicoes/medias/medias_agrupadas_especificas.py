import dask.dataframe as dd

from edicoes.medias.media_agrupada import media_agrupada

def media_mensal_A(df: dd.DataFrame) -> dd.DataFrame:
    """
    
    """
    
    categoria_de_agrupamento: list = ["mes", "h"]
    colunas_remover = ["dia", "hora_str", "tempo_bras", "data_bras", "hora"]

    media = media_agrupada(df, categoria_de_agrupamento, colunas_remover)

    return media


if __name__ == "__main__":
    from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral
    df = ler_dataframes_pontuais_plataformas_geral("p7")
    media = media_mensal_A(df)
    print(media.compute().tail(50))
    print(media[media["ano"] == 2023].compute())