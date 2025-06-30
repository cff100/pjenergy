from pathlib import Path
from pandas.api.types import CategoricalDtype
# Módulos internos do projeto
from obtaining_and_manipulating_data.dataframes.ler_dataframe import ler_dataframe_dask
from config.paths import DIRETORIO_DATAFRAME_PRIMARIO, DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS
from config.constants import ParametrosObtencaoDados as pod

def adiciona_colunas_tempo(diretorio_dataframe_primario: Path = DIRETORIO_DATAFRAME_PRIMARIO, diretorio_dataframe_com_colunas_temporais: Path = DIRETORIO_DATAFRAME_COM_COLUNAS_TEMPORAIS):
    """
    Lê um DataFrame Dask a partir de arquivos Parquet e adiciona colunas derivadas da coluna 'valid_time'.
    """

    # Lê o DataFrame
    df = ler_dataframe_dask(diretorio_dataframe_primario)

    # Extrai componentes da data
    df["ano"] = df["valid_time"].dt.year
    df["mes"] = df["valid_time"].dt.month
    df["dia"] = df["valid_time"].dt.day
    df["hora"] = df["valid_time"].dt.hour.astype(str).str.zfill(2) + ":" + df["valid_time"].dt.minute.astype(str).str.zfill(2)  # Formata a hora como string com dois dígitos
 
    numero_para_mes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    # Converte número do mês para nome do mês
    df["mes_nome"] = df["valid_time"].dt.month.map(numero_para_mes, meta=("mes_nome", "object"))
    
    # Salva sobrescrevendo o diretório destino
    df.to_parquet(diretorio_dataframe_com_colunas_temporais, overwrite=True)

    return df


if __name__ == "__main__":
    # Executa a função para adicionar colunas de tempo
    df = adiciona_colunas_tempo()
    
    # Exibe as primeiras linhas do DataFrame atualizado
    print(df.head())
    