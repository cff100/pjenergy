import dask.dataframe as dd
from pathlib import Path
# Módulos internos do projeto
from config.paths import DIRETORIO_DATAFRAME_NOVAS_COLUNAS

def ler_dataframe_dask(diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS):
    """Ler o dataframe dask composto por arquivos parquet."""
    
    df = dd.read_parquet(diretorio_dados_parquet)
    return df





if __name__ == "__main__":

    # VER OS DADOS

    df = ler_dataframe_dask()

    ## Head (de todo o dataframe)

    print("\n -> -> -> Head:\n")
    print(df.head())

    ## Tail (de todo o dataframe)

    print("\n -> -> -> Tail:\n")
    print(df.tail())
    print("\n \n \n")

    ## Dados de uma partição específica "n_particao"
    n_particao = 30
    df_n = df.partitions[n_particao] # Metadados da partição
    df_n = df_n.compute() # Computa a partição
    print(f"\n -> -> -> Partição {n_particao}:\n")
    print(df_n)
    print("\n \n \n")
    
    ## Uma amostra aleatória dos dados (de todo o dataframe)

    amostra_aleatoria = df.sample(frac=0.000001) # Pega os metadados da estrutura
    amostra_aleatoria = amostra_aleatoria.compute() # Pega os dados em si
    print(" -> -> -> Amostra aleatória:")
    print(amostra_aleatoria)
    print("\n \n \n")



    # OBTER INFORMAÇÕES DE TIPOS, COLUNAS, DTYPES, ETC

    ## Colunas do dataframe

    colunas = df.columns.tolist()
    print(" -> -> -> Lista de colunas de um dataframe:\n")
    print(colunas)
    print("\n -> -> -> Tipos das colunas:\n")
    print(df.dtypes)
    print("\n \n \n")

    ## Número de linhas e colunas do dataframe:
    num_linhas = df.shape[0] # Metadados das linhas
    num_linhas = num_linhas.compute()  # Computa o número de linhas
    num_colunas = df.shape[1]  # Número de colunas é uma propriedade
    print(f" -> -> -> Número de linhas do dataframe: {num_linhas}\n")
    print(f"\n -> -> -> Número de colunas do dataframe: {num_colunas}")
    print("\n \n \n")

    # INFORMAÇÕES ESTATÍSTICAS E ESTRUTURAIS 

    # Resumo do dataframe

    resumo = df.describe() # Metadados do resumo
    resumo = resumo.compute() # Computa o resumo
    print(" -> -> -> Resumo:\n")
    print(resumo)
    print("\n \n \n")

    numero_particoes = df.npartitions
    print(f" -> -> -> Número de partições: {numero_particoes}")
    print("\n \n \n")


    # OUTROS MÉTODOS ÚTEIS

    ## Filtros
    from config.constants import NomeColunasDataframe as ncd
    hora = "03:00"
    df_hora_filtrada = df[df[ncd.hora] == hora].compute()
    print(f" -> -> -> Filtro da hora {hora}\n")
    print(df_hora_filtrada)

    velocidade_limite = 20
    df_velocidade_filtrada = df[df[ncd.velocidade_resultante] >= velocidade_limite].compute()
    print(f"\n\n -> -> -> Filtro de velocidades iguais ou maiores de {velocidade_limite}\n")
    print(df_velocidade_filtrada)
