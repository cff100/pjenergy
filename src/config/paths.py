from pathlib import Path

CAMINHO_BASE_GERAL = Path(__file__).parent.parent.parent # Caminho do projeto

CAMINHO_DADOS = CAMINHO_BASE_GERAL / "data"  # Caminho da pasta de dados
CAMINHO_DADOS_NC = CAMINHO_DADOS / "nc_files" # Caminhos da pasta de dados .nc

#print(CAMINHO_ARQUIVO_NC)