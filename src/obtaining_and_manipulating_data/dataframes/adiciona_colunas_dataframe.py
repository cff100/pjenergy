from pathlib import Path
import dask.dataframe as dd
# Módulos internos do projeto
from obtaining_and_manipulating_data.dataframes.ler_dataframe import ler_dataframe_dask
from obtaining_and_manipulating_data.dataframes.salva_dataframe_substituindo import salva_dataframe_substituindo
from config.paths import DIRETORIO_DATAFRAME_PRIMARIO, DIRETORIO_DATAFRAME_NOVAS_COLUNAS


def adiciona_colunas_tempo(diretorio_dataframe_original: Path = DIRETORIO_DATAFRAME_PRIMARIO, diretorio_dataframe_resultante: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """
    Lê um DataFrame Dask a partir de arquivos Parquet e adiciona colunas derivadas da coluna 'valid_time'.
    """

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe_original)

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
    
    # Salva
    df.to_parquet(diretorio_dataframe_resultante, overwrite=True)

    return df


def adiciona_coluna_velocidade_resultante(diretorio_dataframe_original: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """Calcula e adiciona uma coluna de velocidade resultante"""

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe_original)

    df["Vel"] = (df["u"]**2 + df["v"]**2)**0.5

    # Salva dataframe substituindo o original
    salva_dataframe_substituindo(df, diretorio_dataframe_original)

    return df


# FUNÇÃO PRINCIPAL

def adiciona_colunas_novas() -> dd.DataFrame:
    """Cria um dataframe com colunas novas"""

    df = adiciona_colunas_tempo()
    df = adiciona_coluna_velocidade_resultante()

    return df


if __name__ == "__main__":
    # Executa a função para adicionar colunas de tempo
    df = adiciona_colunas_novas()

    # Exibe as primeiras linhas do DataFrame atualizado
    print(df.head())
    