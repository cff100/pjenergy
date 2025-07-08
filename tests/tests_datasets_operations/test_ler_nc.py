# Módulos internos do projeto
from datasets_operations.ler_nc import ler_dataset_nc_relativo
from config.paths import DIRETORIO_TESTES_ARQUIVOS_NOVOS

def test_ler_nc_infomacoes_principais():
    """Teste para verificar a leitura de informações principais de um arquivo .nc"""

    # Caminho base e o caminho do arquivo .nc a ser lido relativo a essa base
    caminho_base = DIRETORIO_TESTES_ARQUIVOS_NOVOS
    arquivo_nc_caminho_relativo = "teste.nc"

    # Ler as informações principais do arquivo .nc
    ds = ler_dataset_nc_relativo(arquivo_nc_caminho_relativo, caminho_base)
    print("Informações principais do arquivo .nc:")
    print(ds)

    print("Teste de leitura de informações principais do arquivo .nc concluído com sucesso.")