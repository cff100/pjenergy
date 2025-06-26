
"""Para obtenção  de dados de um dataset do Climate Data Store"""
from config.constants import ParametrosObtencaoDados as pod
import cdsapi
import config.paths as paths

def requisicao_dados(nome_arquivo_nc, variaveis, anos, pressao_niveis, meses = pod.meses, dias = pod.dias, utc_horas = pod.horas, area = pod.area, data_format = pod.data_format, download_format = pod.download_format):
    """Requisita dados do Climate Data Store (CDS) e salva em um arquivo .nc."""

    # Inicializar API do CDS
    c = cdsapi.Client() # Exige que o url e a key já estejam configurados em um arquivo .cdsapirc externo.
    
    # Requisição dos dados
    dataset = 'reanalysis-era5-pressure-levels'
    request = {
    'product_type': ['reanalysis'],
    'variable': variaveis,
    'year': anos,
    'month': meses,
    'day': dias,
    'time': utc_horas,
    'area': area,  
    'pressure_level': pressao_niveis,  # Em hPa
    'data_format': data_format,
    'download_format': download_format
    }

    c.retrieve(dataset, request, nome_arquivo_nc)



def requisicao_todos_dados():
    """Faz loops para a obtenção de vários arquivos .nc"""

    n_variaveis = len(pod.variaveis)
    n_anos = len(pod.anos)
    n_pressao_niveis = len(pod.pressao_niveis)
    n_requisicoes = n_variaveis * n_anos * n_pressao_niveis
    requisicao_atual = 0

    for variavel in pod.variaveis:
        for ano in pod.anos:
            for pressao_nivel in pod.pressao_niveis:
                
                arquivo_nc_nome = f"(var-{variavel})_(anos-{ano})_(pressao-{pressao_nivel}).nc"
                print(f"\n Nome do próximo arquivo: {arquivo_nc_nome}\n")

                # Verifica se o arquivo já existe
                # Se existir, pula o download
                if arquivo_existe(arquivo_nc_nome):
                    print(f"\nArquivo {arquivo_nc_nome} já existe. Pulando download.\n")
                    requisicao_atual += 1
                    porcentagem_cumprida = progresso_requisicao(n_requisicoes, requisicao_atual)
                    print(f"Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)\n")
                    continue

                arquivo_nc_caminho = paths.CAMINHO_DADOS_NC / arquivo_nc_nome
                requisicao_dados(arquivo_nc_caminho, variavel, ano, pressao_nivel)

                print(f"\nArquivo {arquivo_nc_nome} baixado com sucesso")
                requisicao_atual += 1
                porcentagem_cumprida = progresso_requisicao(n_requisicoes, requisicao_atual)
                print(f"Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)\n")

    print("Todos os arquivos .nc foram baixados com sucesso.")


def progresso_requisicao(n_requisicoes, requisicao_atual):
    porcentagem_cumprida = round(100 * requisicao_atual/n_requisicoes, 2)
    return porcentagem_cumprida

def arquivo_existe(nome_arquivo):
    """Verifica se o arquivo existe no caminho especificado."""
    caminho_arquivo = paths.CAMINHO_DADOS_NC / nome_arquivo
    return caminho_arquivo.exists()