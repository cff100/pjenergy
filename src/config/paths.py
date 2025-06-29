from pathlib import Path
from config.constants import ConstantesString as cs

CAMINHO_BASE_GERAL = Path(__file__).parent.parent.parent # Caminho do projeto

CAMINHO_DADOS = CAMINHO_BASE_GERAL / "data"  # Diretório da pasta de dados
CAMINHO_DADOS_NC = CAMINHO_DADOS / "nc_files" # Diretório da pasta de dados .nc
CAMINHO_NC_UNICO = CAMINHO_DADOS_NC / cs.NOME_PADRAO_ARQUIVO_NC_UNICO # Caminho do arquivo .nc único
CAMINHO_DADOS_PARQUET = CAMINHO_DADOS / "parquet_files"  # Diretório da pasta de dados parquet

CAMINHO_TESTES = CAMINHO_BASE_GERAL / "tests"  # Diretório da pasta de testes
CAMINHO_TESTES_ARQUIVOS_NOVOS = CAMINHO_TESTES / "new_tests_files" # Diretório de arquivos criados em testes

#print(CAMINHO_ARQUIVO_NC)