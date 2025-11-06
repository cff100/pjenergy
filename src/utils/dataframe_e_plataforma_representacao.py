import dask.dataframe as dd
from typing import Optional, cast

from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral


def resolve_dataframe_e_plataforma_representação(plataforma_representacao: Optional[str], 
                                                 df: Optional[dd.DataFrame]):

    valores = [plataforma_representacao, df] 
    valores_bool = [v is None for v in valores]
    #print(plataforma_representacao)
    #print(df)
    #print(valores_bool)

    if not (any(valores_bool) and not all(valores_bool)):
        raise TypeError("Obrigatoriamente, a dupla de parâmetros 'plataforma_representacao' e 'df' " \
        "devem ter exatamente um dos dois com valor None.")
    elif isinstance(df, dd.DataFrame):
        pass # df é o df passado como parâmetro
    else: 
        plataforma_representacao = cast(str, plataforma_representacao)
        df = ler_dataframes_pontuais_plataformas_geral(plataforma_representacao)

    return df