from typing import Union, Any, Optional, Literal, cast
import dask.dataframe as dd

from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral
from config.constants import Correspondencias as cr


def filtro_especifico(coluna_de_filtragem: str, 
                      objetos_de_filtragem: Union[Any, list], 
                      plataforma_representacao: Optional[str] = None, 
                      df: Optional[dd.DataFrame] = None) -> dd.DataFrame:
    """Filtra um dataframe por um objeto de filtragem.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        coluna_de_filtragem (str): Nome da colona em que se deseja aplicar o filtro
        objetos_de_filtragem (Any | list): Objeto ou lista de objeto pelos quais se deseja filtrar.
        df (Optional[dd.DataFrame]): Dataframe que se deseja filtrar.
    """

    if isinstance(df, dd.DataFrame):
        pass # df é o df passado como parâmetro
    elif df == None and plataforma_representacao == None:
        raise TypeError("Obrigatoriamente, a dupla de parâmetros 'plataforma_representacao' e 'df' " \
        "devem ter no máximo um dos dois com valor None.")
    else: 
        plataforma_representacao = cast(str, plataforma_representacao)
        df = ler_dataframes_pontuais_plataformas_geral(plataforma_representacao)

    if objetos_de_filtragem != None:
        df_filtrado = df[df[coluna_de_filtragem].isin(objetos_de_filtragem) if isinstance(objetos_de_filtragem, list) else df[coluna_de_filtragem] == objetos_de_filtragem]
    else: 
        df_filtrado = df


    print(df_filtrado.compute())
    return df_filtrado




def filtro_faixa_de_valores(coluna_de_filtragem: str,
                            maior_igual_a: Optional[int] = None, 
                            menor_igual_a: Optional[int] = None, 
                            plataforma_representacao: Optional[str] = None, 
                            df: Optional[dd.DataFrame] = None) -> dd.DataFrame:
    
    if isinstance(df, dd.DataFrame):
        pass # df é o df passado como parâmetro
    elif df == None and plataforma_representacao == None:
        raise TypeError("Obrigatoriamente, a dupla de parâmetros 'plataforma_representacao' e 'df' " \
        "devem ter no máximo um dos dois com valor None.")
    else: 
        plataforma_representacao = cast(str, plataforma_representacao)
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
    print(df_filtrado.compute())

    return df_filtrado


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------


def filtra_ano(anos: Optional[Union[int, list]], 
               plataforma_representacao: Optional[str] = None, 
               df: Optional[dd.DataFrame] = None) -> dd.DataFrame:
    """Filtra um dataframe por um ano ou lista de anos.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        anos (int | list): Ano ou lista de anos pelas quais se deseja filtrar.
    """

    df_filtrado = filtro_especifico(cr.DadosVariaveis.ANO, anos, plataforma_representacao, df)

    return df_filtrado



def filtra_estacao(estacoes: Optional[Union[str, list]], 
               plataforma_representacao: Optional[str] = None, 
               df: Optional[dd.DataFrame] = None) -> dd.DataFrame:
    """Filtra um dataframe por uma estação ou lista de estações.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        estacoes (str | list): Estação ou lista de estações pelas quais se deseja filtrar.
    """

    df_filtrado = filtro_especifico(cr.DadosVariaveis.ESTACAO_DO_ANO, estacoes, plataforma_representacao, df)

    return df_filtrado


def filtra_mes(meses: Optional[Union[str, int, list]], 
               plataforma_representacao: Optional[str] = None, 
               df: Optional[dd.DataFrame] = None) -> dd.DataFrame:
    """Filtra um dataframe por um mês ou lista de meses.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        meses (str | int | list): Mês ou lista de meses pelos quais se deseja filtrar.
    """
    if ( isinstance(meses, list) and all(isinstance(mes, int) for mes in meses) ) or isinstance(meses, int):
        df_filtrado = filtro_especifico(cr.DadosVariaveis.MES, meses, plataforma_representacao, df)
    elif ( isinstance(meses, list) and all(isinstance(mes, str) for mes in meses) ) or isinstance(meses, str):
        df_filtrado = filtro_especifico(cr.DadosVariaveis.MES_STR, meses, plataforma_representacao, df)
    elif meses == None:
        df_filtrado = df
    else:
        raise TypeError("O(s) mes(es) que se deseja filtrar devem ser do tipo int, " \
        "str ou uma lista inteiramente de elementos int ou inteiramente de elementos str")
    
    df_filtrado = cast(dd.DataFrame, df_filtrado)
    return df_filtrado


def filtra_hora(horas: Optional[Union[str, int, list]], 
               plataforma_representacao: Optional[str] = None, 
               df: Optional[dd.DataFrame] = None) -> dd.DataFrame:
    """Filtra um dataframe por uma hora ou lista de horas.
    
    Args:
        plataforma_representacao (str): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
        horas (str | int | list): Hora ou lista de horas pelas quais se deseja filtrar.
    """
    if ( isinstance(horas, list) and all(isinstance(mes, int) for mes in horas) ) or isinstance(horas, int):
        df_filtrado = filtro_especifico(cr.DadosVariaveis.HORA, horas, plataforma_representacao, df)
    elif ( isinstance(horas, list) and all(isinstance(mes, str) for mes in horas) ) or isinstance(horas, str):
        df_filtrado = filtro_especifico(cr.DadosVariaveis.HORA_STR, horas, plataforma_representacao, df)
    elif horas == None:
        df_filtrado = df
    else:
        raise TypeError("A(s) hora(s) que se deseja filtrar devem ser do tipo int, " \
        "str ou uma lista inteiramente de elementos int ou inteiramente de elementos str")
    
    df_filtrado = cast(dd.DataFrame, df_filtrado)
    return df_filtrado



def filtra_velocidade_vento(componente: Literal["u","v", "resultante"] = "resultante", 
                            maior_igual_a: Optional[int] = None, 
                            menor_igual_a: Optional[int] = None, 
                            plataforma_representacao: Optional[str] = None, 
                            df: Optional[dd.DataFrame] = None) -> dd.DataFrame:

    """Filtra um dataframe por valores de velocidade do vento.
    """

    if componente == "u":
        coluna_de_filtragem = cr.DadosVariaveis.VELOCIDADE_U
    elif componente == "v":
        coluna_de_filtragem = cr.DadosVariaveis.VELOCIDADE_V
    elif componente == "resultante":
        coluna_de_filtragem = cr.DadosVariaveis.VELOCIDADE_RESULTANTE


    df_filtrado = filtro_faixa_de_valores(coluna_de_filtragem, 
                                          maior_igual_a, 
                                          menor_igual_a, 
                                          plataforma_representacao, 
                                          df)

    return df_filtrado


def filtra_temperatura(maior_igual_a: Optional[int] = None, 
                       menor_igual_a: Optional[int] = None, 
                       plataforma_representacao: Optional[str] = None, 
                       df: Optional[dd.DataFrame] = None) -> dd.DataFrame:

    """Filtra um dataframe por valores de temperatura do ar.
    """
    coluna_de_filtragem = cr.DadosVariaveis.TEMPERATURA_CELSIUS

    df_filtrado = filtro_faixa_de_valores(coluna_de_filtragem, 
                                          maior_igual_a, 
                                          menor_igual_a, 
                                          plataforma_representacao, 
                                          df)
    
    return df_filtrado


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------

def filtragem_abrangente(anos: Optional[Union[int, list]] = None, 
                         estacoes: Optional[Union[str, list]] = None, 
                         meses: Optional[Union[str, int, list]] = None, 
                         horas:  Optional[Union[str, int, list]] = None, 
                         velocidade_componente: Literal["u","v", "resultante"] = "resultante",
                         velocidade_maior_igual_a: Optional[int] = None, 
                         velocidade_menor_igual_a: Optional[int] = None, 
                         temperatura_maior_igual_a: Optional[int] = None, 
                         temperatura_menor_igual_a: Optional[int] = None,
                         plataforma_representacao: Optional[str] = None, 
                         df: Optional[dd.DataFrame] = None) -> dd.DataFrame:
    

    dicionario_funcoes_argumentos = {filtra_ano: anos, 
                                    filtra_estacao: estacoes, 
                                    filtra_mes: meses, 
                                    filtra_hora: horas, 
                                    filtra_velocidade_vento: (velocidade_componente, velocidade_maior_igual_a, velocidade_menor_igual_a), 
                                    filtra_temperatura: (temperatura_maior_igual_a, temperatura_menor_igual_a)
                                    }  
    
    df_filtrado = df
    for funcao in dicionario_funcoes_argumentos.keys():
        argumentos = dicionario_funcoes_argumentos[funcao]
        print(argumentos)
        if isinstance(argumentos, tuple):
            df_filtrado = funcao(*argumentos, plataforma_representacao, df_filtrado)
        else:
            df_filtrado = funcao(argumentos, plataforma_representacao, df_filtrado)

    df_filtrado = cast(dd.DataFrame, df_filtrado)
    return df_filtrado



if __name__ == "__main__":

    import pandas as pd
    pd.set_option('display.max_columns', None)

    # df_filtrado = filtra_ano([2020, 2024, 2017], plataforma_representacao = "p7")
    # print(f'Filtrado por anos:\n {df_filtrado.compute()}\n')

    # df_filtrado = filtra_estacao("Outono", plataforma_representacao = "p7")
    # print(f'Filtrado por estações:\n {df_filtrado.compute()}\n')

    # df_filtrado = filtra_mes([8, 4], plataforma_representacao = "p7")
    # print(f'Filtrado por meses:\n {df_filtrado.compute()}\n')

    # df_filtrado = filtra_hora([6], plataforma_representacao = "p7")
    # print(f'Filtrado por horas:\n {df_filtrado.compute()}\n')

    # df_filtrado = filtra_velocidade_vento(menor_igual_a = 14, plataforma_representacao = "p7")
    # print(f'Filtrado por velocidades do vento:\n {df_filtrado.compute()}\n')

    # #print(df_filtrado["t_C"].compute().min())
    # #print(df_filtrado["t_C"].compute().max())

    # df_filtrado = filtra_temperatura(maior_igual_a = 25, plataforma_representacao = "p7")
    # print(f'Filtrado por temperaturas:\n {df_filtrado.compute()}\n')

    # print(f'Tipos:\n {df_filtrado.dtypes}\n')
    
    df_filtrado = filtragem_abrangente(horas = 5, estacoes= "Inverno", plataforma_representacao = "p7")
    print(f'Filtragem abrangente:\n {df_filtrado.compute()}\n')
    