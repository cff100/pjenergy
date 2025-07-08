# Módulos internos do projeto
import config.paths as paths
from datasets_operations.requisicao_dados import requisicao_dados
from config.constants import ParametrosObtencaoDados as pod
from utils.cria_caminho_arquivo import cria_caminho_arquivo_relativo

def test_requisicao_dados(requisitar = True):
    """Teste para verificar a requisição de dados do Climate Data Store (CDS)"""

    # Variáveis, anos e pressões a serem solicitados
    variavel = pod.variaveis[0]
    ano = pod.anos[0]
    pressao_nivel = pod.pressao_niveis[0]

    print(f" -> -> -> Variáveis escolhidas: {variavel}")
    print(f" -> -> -> Anos escolhidos: {ano}")
    print(f" -> -> -> Pressões escolhidas: {pressao_nivel}")

    # Localização do arquivo de saída
    diretorio_base = paths.DIRETORIO_TESTES_ARQUIVOS_NOVOS
    arquivo_nome = f"teste-(var-{variavel})_(ano-{ano})_(pressao-{pressao_nivel}).nc"
    # Nome alternativo -> arquivo_nc_caminho = f"tests/new_tests_files/teste_(var-{variaveis})_(anos-{anos})_(pressao-{pressao_niveis}).nc"
    
    print(f" -> -> -> Caminho relativo de saída: {arquivo_nome}")

    # Cria o caminho absoluto e confere se o diretório existe
    arquivo_nc_caminho = cria_caminho_arquivo_relativo(arquivo_nome, diretorio_base)
    print(f" -> -> -> Caminho absoluto de saída: {arquivo_nc_caminho}")
    
    if arquivo_nc_caminho.exists():
        print(f" -> -> -> Arquivo {arquivo_nc_caminho} já existe. Pulando download.")
        return
    else:
        print(f" -> -> -> Arquivo {arquivo_nc_caminho} não existe. Iniciando download...")

    if not requisitar:
        print(" -> -> -> ATENÇÃO: Requisição de dados não realizada. Mude o parâmetro 'requisitar' para True para realizar a requisição.")
    else:
        requisicao_dados(variavel, ano, pressao_nivel, diretorio_datasets = arquivo_nc_caminho)
        print(" -> -> -> Iniciando o teste de requisição de dados...")