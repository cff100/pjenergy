from typing import Union, Any, Optional, Literal, cast
import dask.dataframe as dd

from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral
from config.constants import Correspondencias as cr

def filtro(plataforma_representacao: str, coluna_de_filtragem: str, objetos_de_filtragem: Union[Any, list]) -> dd.DataFrame:
    """Filtra um dataframe por um objeto de filtragem.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        coluna_de_filtragem (str): Nome da colona em que se deseja aplicar o filtro
        objetos_de_filtragem (Any | list): Objeto ou lista de objeto pelos quais se deseja filtrar.
    """

    df = ler_dataframes_pontuais_plataformas_geral(plataforma_representacao)

    df_filtrado = df[df[coluna_de_filtragem].isin(objetos_de_filtragem) if isinstance(objetos_de_filtragem, list) else df[coluna_de_filtragem] == objetos_de_filtragem]
    return df_filtrado


def filtra_estacao(plataforma_representacao: str, estacoes: Union[str, list]) -> dd.DataFrame:
    """Filtra um dataframe por uma estação ou lista de estações.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        estacoes (str | list): Estação ou lista de estações pelas quais se deseja filtrar.
    """

    df_filtrado = filtro(plataforma_representacao, cr.DadosVariaveis.ESTACAO_DO_ANO, estacoes )

    return df_filtrado


def filtra_ano(plataforma_representacao: str, anos: Union[int, list]) -> dd.DataFrame:
    """Filtra um dataframe por um ano ou lista de anos.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        anos (int | list): Ano ou lista de anos pelas quais se deseja filtrar.
    """

    df_filtrado = filtro(plataforma_representacao, cr.DadosVariaveis.ANO, anos )

    return df_filtrado


def filtra_mes(plataforma_representacao: str, meses: Union[str, int, list]) -> dd.DataFrame:
    """Filtra um dataframe por um mês ou lista de meses.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        meses (str | int | list): Mês ou lista de meses pelos quais se deseja filtrar.
    """
    if ( isinstance(meses, list) and all(isinstance(mes, int) for mes in meses) ) or isinstance(meses, int):
        df_filtrado = filtro(plataforma_representacao, cr.DadosVariaveis.MES, meses)
    elif ( isinstance(meses, list) and all(isinstance(mes, str) for mes in meses) ) or isinstance(meses, str):
        df_filtrado = filtro(plataforma_representacao, cr.DadosVariaveis.MES_STR, meses)
    else:
        raise TypeError("O(s) mes(es) que se deseja filtrar devem ser do tipo int, " \
        "str ou uma lista inteiramente de elementos int ou inteiramente de elementos str")
    
    return df_filtrado


def filtra_hora(plataforma_representacao: str, horas: Union[str, int, list]) -> dd.DataFrame:
    """Filtra um dataframe por uma hora ou lista de horas.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        horas (str | int | list): Hora ou lista de horas pelas quais se deseja filtrar.
    """
    if ( isinstance(horas, list) and all(isinstance(mes, int) for mes in horas) ) or isinstance(horas, int):
        df_filtrado = filtro(plataforma_representacao, cr.DadosVariaveis.HORA, horas)
    elif ( isinstance(horas, list) and all(isinstance(mes, str) for mes in horas) ) or isinstance(horas, str):
        df_filtrado = filtro(plataforma_representacao, cr.DadosVariaveis.HORA_STR, horas)
    else:
        raise TypeError("A(s) hora(s) que se deseja filtrar devem ser do tipo int, " \
        "str ou uma lista inteiramente de elementos int ou inteiramente de elementos str")
    
    return df_filtrado



def filtra_velocidade_vento(plataforma_representacao: str, componente: Literal["u","v", "resultante"] = "resultante", 
                            maior_igual_a: Optional[int] = None, menor_igual_a: Optional[int] = None) -> dd.DataFrame:

    """Filtra um dataframe por valores de velocidade do vento.
    """

    if componente == "u":
        coluna_de_filtragem = cr.DadosVariaveis.VELOCIDADE_U
    elif componente == "v":
        coluna_de_filtragem = cr.DadosVariaveis.VELOCIDADE_V
    elif componente == "resultante":
        coluna_de_filtragem = cr.DadosVariaveis.VELOCIDADE_RESULTANTE


    df = ler_dataframes_pontuais_plataformas_geral(plataforma_representacao)
    if maior_igual_a is not None and menor_igual_a is not None:
        df_filtrado = df[(df[coluna_de_filtragem] >= maior_igual_a) & (df[coluna_de_filtragem] <= menor_igual_a)]
    elif maior_igual_a is not None:
        df_filtrado = df[df[coluna_de_filtragem] >= maior_igual_a]
    elif menor_igual_a is not None:
        df_filtrado = df[df[coluna_de_filtragem] <= menor_igual_a]
    else:
        df_filtrado = df

    df_filtrado = cast(dd.DataFrame, df_filtrado)
    return df_filtrado


if __name__ == "__main__":

    import pandas as pd
    pd.set_option('display.max_columns', None)

    #df_filtrado = filtra_ano("p7", [2020, 2024, 2017])
    #df_filtrado = filtra_estacao("p7", ["Outono", "Inverno"])
    #df_filtrado = filtra_mes("p7", [8, 4])
    #df_filtrado = filtra_hora("p7", [6])

    df_filtrado = filtra_velocidade_vento("p7")
    print(df_filtrado["vel_res"].compute().min())
    print(df_filtrado["vel_res"].compute().max())
    df_filtrado = filtra_velocidade_vento("p7", menor_igual_a = 1)
    print(df_filtrado.compute())
    print(df_filtrado.dtypes)
    