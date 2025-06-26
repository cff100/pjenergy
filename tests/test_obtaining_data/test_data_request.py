from obtaining_data.data_request import requisicao_dados
from config.constants import ParametrosObtencaoDados as pod
import os

def test_requisicao_dados(requisitar = True):
    """Teste para verificar a requisição de dados do Climate Data Store (CDS)"""

    # Variáveis, anos e pressões a serem solicitados
    variaveis = pod.variaveis[0]
    anos = pod.anos[0]
    pressao_niveis = pod.pressao_niveis[0]

    print(f"Variáveis escolhidas: {variaveis}")
    print(f"Anos escolhidos: {anos}")
    print(f"Pressões escolhidas: {pressao_niveis}")

    # Localização do arquivo de saída
    arquivo_nc_caminho = f"tests/new_tests_files/teste.nc"
    # Nome alternativo -> arquivo_nc_caminho = f"tests/new_tests_files/teste_(var-{variaveis})_(anos-{anos})_(pressao-{pressao_niveis}).nc"
    # Remover espaços
    arquivo_nc_caminho = arquivo_nc_caminho.replace(" ", "_")
    print(f"Nome do arquivo de saída: {arquivo_nc_caminho}")

    # Garante que o diretório existe
    os.makedirs(os.path.dirname(arquivo_nc_caminho), exist_ok=True)

    if not requisitar:
        print("ATENÇÃO: Requisição de dados não realizada. Mude o parâmetro 'requisitar' para True para realizar a requisição.")
    else:
        requisicao_dados(arquivo_nc_caminho, variaveis, anos, pressao_niveis)
        print("Iniciando o teste de requisição de dados...")