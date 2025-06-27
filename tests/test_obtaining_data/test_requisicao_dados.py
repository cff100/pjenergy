from obtaining_data.requisicao_dados import requisicao_dados
from config.constants import ParametrosObtencaoDados as pod
import config.paths as paths
from pathlib import Path

def test_requisicao_dados(requisitar = False):
    """Teste para verificar a requisição de dados do Climate Data Store (CDS)"""

    # Variáveis, anos e pressões a serem solicitados
    variaveis = pod.variaveis[0]
    anos = pod.anos[0]
    pressao_niveis = pod.pressao_niveis[0]

    print(f" -> -> -> Variáveis escolhidas: {variaveis}")
    print(f" -> -> -> Anos escolhidos: {anos}")
    print(f" -> -> -> Pressões escolhidas: {pressao_niveis}")

    # Localização do arquivo de saída
    arquivo_nc_caminho_relativo = f"tests/new_tests_files/teste.nc"
    # Nome alternativo -> arquivo_nc_caminho = f"tests/new_tests_files/teste_(var-{variaveis})_(anos-{anos})_(pressao-{pressao_niveis}).nc"

    print(f" -> -> -> Caminho relativo de saída: {arquivo_nc_caminho_relativo}")

    # Cria o caminho absoluto e confere se o diretório existe
    arquivo_nc_caminho = paths.CAMINHO_BASE_GERAL / arquivo_nc_caminho_relativo
    if arquivo_nc_caminho.exists():
        print(f" -> -> -> Arquivo {arquivo_nc_caminho} já existe. Pulando download.")
        return
    else:
        print(f" -> -> -> Arquivo {arquivo_nc_caminho} não existe. Iniciando download...")

    if not requisitar:
        print(" -> -> -> ATENÇÃO: Requisição de dados não realizada. Mude o parâmetro 'requisitar' para True para realizar a requisição.")
    else:
        requisicao_dados(arquivo_nc_caminho, variaveis, anos, pressao_niveis)
        print(" -> -> -> Iniciando o teste de requisição de dados...")