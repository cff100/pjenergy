import dask.dataframe as dd
from pathlib import Path
# Módulos internos do projeto
from obtaining_and_manipulating_data.dataframes.ler_dataframe import ler_dataframe_dask
from config.paths import DIRETORIO_DATAFRAME_PRIMARIO

def adiciona_colunas_tempo(diretorio_dados_parquet: Path = DIRETORIO_DATAFRAME_PRIMARIO):
    """
    Lê um DataFrame Dask a partir de arquivos Parquet e adiciona colunas derivadas da coluna 'valid_time'.
    Sobrescreve o diretório original com os dados atualizados.
    """

    # Lê o DataFrame
    df = ler_dataframe_dask(diretorio_dados_parquet)

    # Extrai componentes da data
    df["ano"] = df["valid_time"].dt.year # Cria a coluna de ano
    df["dia"] = df["valid_time"].dt.day # Cria a coluna de dia
    df["hora"] = df["valid_time"].dt.hour # Cria a coluna de hora

    # Dicionário com nomes dos meses
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    # Cria coluna de meses
    df["mes"] = df["valid_time"].dt.month.map(meses, meta=('valid_time', 'object'))

    # Categoriza colunas que se beneficiam disso
    df = df.categorize(columns=["ano", "dia", "hora", "mes"])

    # Salva sobrescrevendo os arquivos parquet
    df.to_parquet(diretorio_dados_parquet, overwrite=True)

    return df

# CONCERTAR FUNÇÃO

if __name__ == "__main__":
    # Executa a função para adicionar colunas de tempo
    df_atualizado = adiciona_colunas_tempo()
    
    # Exibe as primeiras linhas do DataFrame atualizado
    print(df_atualizado.head())
    