from utils.ler_nc import ler_nc_infomacoes_principais

def test_ler_nc_infomacoes_principais():
    """Teste para verificar a leitura de informações principais de um arquivo .nc"""

    # Caminho do arquivo .nc a ser lido
    arquivo_nc_caminho = "tests/new_tests_files/teste.nc"

    # Ler as informações principais do arquivo .nc
    ds = ler_nc_infomacoes_principais(arquivo_nc_caminho)
    print("Informações principais do arquivo .nc:")
    print(ds)

    print("Teste de leitura de informações principais do arquivo .nc concluído com sucesso.")