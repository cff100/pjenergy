from pathlib import Path
import dask.dataframe as dd
from dask.diagnostics.progress import ProgressBar
# Módulos internos do projeto
from inicial_data_operations.dataframes.ler_dataframe import ler_dataframe_dask
from inicial_data_operations.dataframes.salva_dataframe_substituindo import salva_dataframe_substituindo
from config.paths import DIRETORIO_DATAFRAME_PRIMARIO, DIRETORIO_DATAFRAME_NOVAS_COLUNAS

def copia_dataframe_primario(diretorio_dataframe_primario: Path = DIRETORIO_DATAFRAME_PRIMARIO, diretorio_dataframe_novas_colunas: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS):
    """Faz uma cópia da pasta do dataframe primário na pasta de dataframe com novas colunas. Serve para iniciar a modificação das colunas."""

    # Lê o dataframe primario
    df = ler_dataframe_dask(diretorio_dataframe_primario)

    # Salva na pasta que será usada
    with ProgressBar(): # Com barra de progresso no terminal
        print("Copiando dataframe primário para pasta que terá o dataframe com colunas editadas...")
        df.to_parquet(diretorio_dataframe_novas_colunas, overwrite = True)
        print("\n")


def remover_colunas_indesejadas(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    df = df.drop(columns = ["number", "expver"])

    ## Salva dataframe substituindo o original
    print("Removendo colunas indesejadas...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df

def adiciona_colunas_tempo(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """
    Lê um DataFrame Dask a partir de arquivos Parquet e adiciona colunas derivadas da coluna 'valid_time'.
    """

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

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
    
    ## Salva dataframe substituindo o original
    print("Adicionando colunas de tempo...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df


def adiciona_coluna_velocidade_resultante(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """Calcula e adiciona uma coluna de velocidade resultante"""

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    df["velocidade"] = (df["u"]**2 + df["v"]**2)**0.5

    # Salva dataframe substituindo o original
    print("Adicionando colunas velocidade resultante...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df

def adiciona_coluna_temperatura_celsius(diretorio_dataframe: Path = DIRETORIO_DATAFRAME_NOVAS_COLUNAS) -> dd.DataFrame:
    """Adiciona uma coluna de temperatura a partir da coluna de temperatura em celsius"""

    # Lê o dataframe original
    df = ler_dataframe_dask(diretorio_dataframe)

    df["t_C"] = df["t"] - 273.15

    # Salva dataframe substituindo o original
    print("Adicionando coluna de temperatura em graus celsius...")
    salva_dataframe_substituindo(df, diretorio_dataframe)
    print("\n")

    return df

# FUNÇÃO PRINCIPAL

def edita_colunas() -> dd.DataFrame:
    """Cria um dataframe com colunas novas"""

    copia_dataframe_primario()

    # Realiza operações sucessivas sobre o dataframe
    remover_colunas_indesejadas()
    adiciona_colunas_tempo()
    adiciona_coluna_velocidade_resultante()
    df = adiciona_coluna_temperatura_celsius()  # Recebe o dataframe depois de todas as modificações

    return df


if __name__ == "__main__":
    # Executa a função para adicionar colunas de tempo
    df = edita_colunas()

    # Exibe as primeiras linhas do DataFrame atualizado
    print(df.head())
    