from utils.ler_nc import ler_nc_infomacoes_principais
from config.paths import CAMINHO_BASE_GERAL

def test_ler_nc_infomacoes_principais():
    """Teste para verificar a leitura de informações principais de um arquivo .nc"""

    # Caminho base e o caminho do arquivo .nc a ser lido relativo a essa base
    caminho_base = CAMINHO_BASE_GERAL 
    arquivo_nc_caminho_relativo = "tests/new_tests_files/teste.nc"

    # Ler as informações principais do arquivo .nc
    ds = ler_nc_infomacoes_principais(arquivo_nc_caminho_relativo, caminho_base)
    print("Informações principais do arquivo .nc:")
    print(ds)

    print("Teste de leitura de informações principais do arquivo .nc concluído com sucesso.")