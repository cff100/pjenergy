from pathlib import Path
from config.constants import ConstantesString as cs, OutrasConstantes as oc

CAMINHO_BASE_GERAL = Path(__file__).parent.parent.parent # Caminho do projeto

# ----------------------

DIRETORIO_DADOS = CAMINHO_BASE_GERAL / "data"  # Diretório da pasta de dados
DIRETORIO_DATASETS = DIRETORIO_DADOS / "datasets" # Diretório da pasta de datasets

DIRETORIO_DATASETS_ORIGINAIS = DIRETORIO_DATASETS / "originals"

CAMINHO_RELATIVO_DATASET_UNIDO = Path("merged/" + cs.NOME_PADRAO_ARQUIVO_NC_UNIDO) # Caminho relativo do arquivo NetCDF unido
CAMINHO_ABSOLUTO_DATASET_UNIDO = DIRETORIO_DATASETS / CAMINHO_RELATIVO_DATASET_UNIDO # Caminho do arquivo NetCDF unido

def caminho_absoluto_dataset_plataforma(plataforma: str | None) -> Path:
    if not plataforma:
        nome_arquivo = "ponto_nao_especifico.nc"
    else:
        nome_arquivo = oc.plataformas_dados[plataforma]["nome_arquivo"]

    CAMINHO_ABSOLUTO_DATASET_PLATAFORMA = DIRETORIO_DATASETS / "plataforms" / nome_arquivo
    
    return CAMINHO_ABSOLUTO_DATASET_PLATAFORMA

# ----------------------

# DIRETORIO_DATAFRAMES = DIRETORIO_DADOS / "dataframes" # Diretório de todos os dataframes
# DIRETORIO_DATAFRAME_PRIMARIO = DIRETORIO_DATAFRAMES / "dataframe_primario"  # Diretório da pasta com o dataframe obtido do arquivo NetCDF único
# DIRETORIO_DATAFRAME_NOVAS_COLUNAS = DIRETORIO_DATAFRAMES / "dataframe_colunas_editadas" # Diretório da pasta com o novo dataframe, com edição, inclusive adição, de novas colunas.

# DIRETORIO_DATAFRAME_TEMPORARIO = DIRETORIO_DATAFRAMES / "dataframe_temporario" # Diretório do dataframe criado temporariamente para operações de edição.

# ----------------------

DIRETORIO_TESTES = CAMINHO_BASE_GERAL / "tests"  # Diretório da pasta de testes
DIRETORIO_TESTES_ARQUIVOS_NOVOS = DIRETORIO_TESTES / "new_tests_files" # Diretório de arquivos criados em testes
