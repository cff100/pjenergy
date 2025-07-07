from pathlib import Path
from config.constants import ConstantesString as cs, OutrasConstantes as oc

CAMINHO_BASE_GERAL = Path(__file__).parent.parent.parent # Caminho do projeto

# ----------------------

DIRETORIO_DADOS = CAMINHO_BASE_GERAL / "data"  # Diretório da pasta de dados

# ----------------------

DIRETORIO_DATASETS = DIRETORIO_DADOS / "datasets" # Diretório da pasta de datasets

DIRETORIO_DATASETS_ORIGINAIS = DIRETORIO_DATASETS / "originals"

CAMINHO_RELATIVO_DATASET_UNIDO = Path("merged/" + cs.NOME_PADRAO_ARQUIVO_NC_UNIDO) # Caminho relativo do arquivo NetCDF unido
CAMINHO_ABSOLUTO_DATASET_UNIDO = DIRETORIO_DATASETS / CAMINHO_RELATIVO_DATASET_UNIDO # Caminho do arquivo NetCDF unido

def caminho_absoluto_dataset_plataforma(plataforma: str | None) -> Path:
    "Decide o nome do caminho a partir do valor de 'plataforma'. """
    if not plataforma:
        nome_arquivo = "ponto_nao_especifico.nc"
    else:
        nome_arquivo = oc.plataformas_dados[plataforma]["nome_arquivo"]

    CAMINHO_ABSOLUTO_DATASET_PLATAFORMA = DIRETORIO_DATASETS / "plataforms" / nome_arquivo
    
    return CAMINHO_ABSOLUTO_DATASET_PLATAFORMA

# ----------------------

DIRETORIO_DATAFRAMES = DIRETORIO_DADOS / "dataframes" # Diretório de todos os dataframes
DIRETORIO_DATAFRAMES_PLATAFORMAS = DIRETORIO_DATAFRAMES / "plataforms"  # Diretório da pasta com os dataframes de pontos específicos

def caminho_absoluto_dataframe_plataforma(plataforma: str | None) -> Path:
    "Decide o nome do caminho a partir do valor de 'plataforma'. """
    if not plataforma:
        nome_arquivo = "ponto_nao_especifico.parquet"
    else:
        nome_arquivo = oc.plataformas_dados[plataforma]["nome_arquivo"]

    CAMINHO_ABSOLUTO_DATASET_PLATAFORMA = DIRETORIO_DATAFRAMES / "plataforms" / nome_arquivo
    
    return CAMINHO_ABSOLUTO_DATASET_PLATAFORMA

# ----------------------

DIRETORIO_TESTES = CAMINHO_BASE_GERAL / "tests"  # Diretório da pasta de testes
DIRETORIO_TESTES_ARQUIVOS_NOVOS = DIRETORIO_TESTES / "new_tests_files" # Diretório de arquivos criados em testes
