import dask.dataframe as dd
from typing import cast

from config.constants import Correspondencias as cr

def media_agrupada(df: dd.DataFrame, 
                   categoria_de_agrupamento: list, 
                   colunas_remover: list, ) -> dd.DataFrame:
    """
    Função geral para fazer média agrupada de valores de um dataframe.

    Args:
        df (dd.Dataframe): Dataframe objeto da média
        categorias_de_agrupamento (lista): Lista com as categorias em relação às quais agrupar.
        colunas_remover (list): Lista com os nomes das colunas a serem removidas. 
            Por exemplo, em uma média diária, a coluna de horas se torna inútil e deve ser eliminada.
    """
    # Lista com os nomes das colunas com valores que deseja se fazer a média.
    colunas_alvo = cr.DadosVariaveis.VARIAVEIS_DE_ANALISE  

    # Remove colunas desnecessárias
    df = df.drop(columns=colunas_remover, errors="ignore")
    # Remove a coluna de tempo em UTC0, já que as médias são feitas considerando o tempo no horário de Brasília, 
    # tornando os valores em outros fusos horários incompatíveis.
    df = df.drop(columns=["tempo_UTC0"], errors="ignore")  

    #print(df.compute())

    todas_colunas = list(df.columns)
    colunas_nao_alvo = [coluna for coluna in todas_colunas if coluna not in colunas_alvo] # Lista de colunas que não se deseja vazer média

    # Criação de dicionário com instruções para o método de média agrupada
    agg_dicio = {col: "mean" for col in colunas_alvo}
    agg_dicio.update({col: "first" for col in colunas_nao_alvo})

    # Cálculo da média agrupada
    media = df.groupby(categoria_de_agrupamento, sort=categoria_de_agrupamento).agg(agg_dicio)
    media = cast(dd.DataFrame, media)
    
    return media


if __name__ == "__main__":
    from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral
    df = ler_dataframes_pontuais_plataformas_geral("p7")
    media = media_agrupada(df, ["data_bras", "h"], ["hora","hora_str"])
    print(media.compute().tail(50))
    print(media.columns)
    print(media)
    print(media[media["data_bras"] == "2016-11-14"].compute())
    print(media[media["ano"] == 2015].compute())