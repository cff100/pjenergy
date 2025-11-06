import dask.dataframe as dd
from typing import cast
import numpy as np

from config.constants import Correspondencias as cr

def listas_para_agrupamento(categorias_de_agrupamento: list): #-> tuple[list, list]
    """Gera, à partir das categorias de agrupamento escolhidas, as listas de colunas a serem removidas do dataframe e a de colunas que receberão argumento 'first' no agrupamento.
    Args:
        categorias_de_agrupamento (lista): Lista com as categorias em relação às quais agrupar.
    """

    # Variáveis ordenadas por abrangência, da mais abrangente para a menos abrtangente
    variaveis_ordenadas_por_abrangencia = ["ano", "estação", "mes", 
                                           "mes_nome", "data_bras", 
                                           "dia", "hora", "hora_str"] 
    
    # Matriz que organiza a relação entre as categorias nas colunas com as categorias das linhas
    # Legenda:
        # S: Superioridade
        # D: Divergência
        # L: Linearidade
        # EQ: Equivalência
    matriz_de_relacoes = np.array([["-", "D", "D", "D", "L", "L", "D", "D"],
                                   ["S", "-", "D", "D", "L", "L", "D", "D"],
                                   ["S", "S", "-", "EQ", "L", "L", "D", "D"],
                                   ["S", "S", "EQ", "-", "L", "L", "D", "D"],
                                   ["S", "S", "S", "S", "-", "L", "D", "D"],
                                   ["S", "S", "S", "S", "S", "-", "D", "D"],
                                   ["S", "S", "S", "S", "S", "S", "-", "EQ"],
                                   ["S", "S", "S", "S", "S", "S", "EQ", "-"]])

    numero_de_linhas_e_colunas = len(matriz_de_relacoes)

    for categoria in variaveis_ordenadas_por_abrangencia: # Varrer todas as variáveis existentes
        if categoria in categorias_de_agrupamento:
            i = variaveis_ordenadas_por_abrangencia.index(categoria) # Pega o número na linha relacionada daquela categoria
            for j in range(numero_de_linhas_e_colunas): # Percorre todas as colunas
                matriz_de_relacoes[i][j] = 0  # Transforma os elementos em 0 para os identificar como a serem desconsiderados

    print(matriz_de_relacoes)


def media_agrupada(df: dd.DataFrame, 
                   categorias_de_agrupamento: list, 
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

    print(df)
    # Remove colunas desnecessárias
    df = df.drop(columns=colunas_remover, errors="ignore")
    # Remove a coluna de tempo em UTC0, já que as médias são feitas considerando o tempo no horário de Brasília, 
    # tornando os valores em outros fusos horários incompatíveis.
    df = df.drop(columns=["tempo_UTC0", "tempo_bras"], errors="ignore")  

    #print(df.compute())

    todas_colunas = list(df.columns)
    colunas_nao_alvo = [coluna for coluna in todas_colunas if coluna not in colunas_alvo] # Lista de colunas que não se deseja vazer média
    print(f"Todas colunas: {todas_colunas}")
    #print(f"Colunas não alvo: {colunas_nao_alvo}")

    # Criação de dicionário com instruções para o método de média agrupada
    agg_dicio = {col: "mean" for col in colunas_alvo}
    agg_dicio.update({col: "first" for col in colunas_nao_alvo})
    #print(f"agg_dicio: {agg_dicio}")

    # Cálculo da média agrupada
    media = df.groupby(categorias_de_agrupamento, sort=categorias_de_agrupamento).agg(agg_dicio)
    media = cast(dd.DataFrame, media)
    
    return media


if __name__ == "__main__":
    from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral
    df = ler_dataframes_pontuais_plataformas_geral("p7")
    media = media_agrupada(df, ["data_bras", "h"], ["hora", "hora_str"])
    print(media.compute().head(50))
    print(media.columns)
    print(media)
    print(media[media["data_bras"] == "2016-11-14"].compute())
    print(media[media["ano"] == 2015].compute())
    # listas_para_agrupamento(["ano", "mes", "h", "hora"])