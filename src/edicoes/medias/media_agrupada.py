import dask.dataframe as dd
from typing import cast

def media_agrupada(df: dd.DataFrame, colunas_remover: list, categoria_de_agrupamento: list = ["data_bras", "h"], colunas_alvo: list = ["vel_u","vel_v","vel_res","t_C","t_K","r"]) -> dd.DataFrame:


    df = df.drop(columns=["tempo_UTC0"], errors="ignore")
    df = df.drop(columns=colunas_remover, errors="ignore")

    #print(df.compute())

    todas_colunas = list(df.columns)
    colunas_nao_alvo = [coluna for coluna in todas_colunas if coluna not in colunas_alvo]

    agg_dicio = {col: "mean" for col in colunas_alvo}
    agg_dicio.update({col: "first" for col in colunas_nao_alvo})

    media = df.groupby(categoria_de_agrupamento, sort=categoria_de_agrupamento).agg(agg_dicio)
    media = cast(dd.DataFrame, media)
    
    return media


if __name__ == "__main__":
    from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral
    df = ler_dataframes_pontuais_plataformas_geral("p7")
    media = media_agrupada(df,["hora","hora_str"])
    print(media.compute().tail(50))
    print(media.columns)
    print(media[media["data_bras"] == "2021-11-14"].compute())