from pathlib import Path
from config.constants import ConstantesString as cs

CAMINHO_BASE_GERAL = Path(__file__).parent.parent.parent # Caminho do projeto

DIRETORIO_DADOS = CAMINHO_BASE_GERAL / "data"  # Diretório da pasta de dados
DIRETORIO_DATASET_NC = DIRETORIO_DADOS / "nc_files" # Diretório da pasta de dados .nc
CAMINHO_NC_UNICO = DIRETORIO_DATASET_NC / cs.NOME_PADRAO_ARQUIVO_NC_UNICO # Caminho do arquivo .nc único
DIRETORIO_DATAFRAME_PRIMARIO = DIRETORIO_DADOS / "dataframe_primario"  # Diretório da pasta de dados parquet

DIRETORIO_TESTES = CAMINHO_BASE_GERAL / "tests"  # Diretório da pasta de testes
DIRETORIO_TESTES_ARQUIVOS_NOVOS = DIRETORIO_TESTES / "new_tests_files" # Diretório de arquivos criados em testes

#print(CAMINHO_ARQUIVO_NC)