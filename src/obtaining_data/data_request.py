
"""Para obtenção  de dados de um dataset do Climate Data Store"""
from config.constants import ParametrosObtencaoDados as pod
import cdsapi
import config.paths as paths
from pathlib import Path

# Funções principais de requisição de dados
# ----------------------------

def requisicao_dados(arquivo_nc_caminho: Path, 
                     variavel: str, # Apenas uma variável por vez, como 'u_component_of_wind'
                     ano: int, # Apenas um ano por vez, como 2020
                     pressao_nivel: int,  # Apenas um nível de pressão por vez, como 900
                     meses: tuple[int, ...] = pod.meses, 
                     dias: tuple[int, ...] = pod.dias, 
                     utc_horas: tuple[str, ...] = pod.horas, 
                     area: tuple[float, float, float, float] = pod.area, 
                     data_format: str = pod.data_format, 
                     download_format: str = pod.download_format): 
    """Requisita dados do Climate Data Store (CDS) e salva em um arquivo .nc."""

    # Inicializar API do CDS
    c = cdsapi.Client() # Exige que o url e a key já estejam configurados em um arquivo .cdsapirc externo.
    
    # Requisição dos dados
    dataset = 'reanalysis-era5-pressure-levels'
    request = {
    'product_type': ['reanalysis'],
    'variable': variavel,
    'year': ano,
    'month': meses,
    'day': dias,
    'time': utc_horas,
    'area': area,  
    'pressure_level': pressao_nivel,  # Em hPa
    'data_format': data_format,
    'download_format': download_format
    }

    c.retrieve(dataset, request, arquivo_nc_caminho)


def requisicao_multiplos_dados(variaveis: tuple[str, ...] = pod.variaveis, 
                            anos: tuple[int, ...] = pod.anos, 
                            pressao_niveis: tuple[int, ...] = pod.pressao_niveis, 
                            meses: tuple[int, ...] = pod.meses, 
                            dias: tuple[int, ...] = pod.dias, 
                            utc_horas: tuple[str, ...] = pod.horas, 
                            area: tuple[float, float, float, float] = pod.area, 
                            data_format: str = pod.data_format, 
                            download_format: str = pod.download_format):
    """Faz loops para a obtenção de vários arquivos .nc de acordo com os valores passados como parâmetros."""

    n_requisicoes = calcula_combinacoes(variaveis, anos, pressao_niveis)
    print(f"\n -> -> -> Número total de requisições: {n_requisicoes}\n")
    requisicao_atual = 0

    for variavel in variaveis:
        for ano in anos:
            for pressao_nivel in pressao_niveis:

                arquivo_nc_nome = nome_arquivo(variavel, ano, pressao_nivel)
                print(f"\n -> -> -> Nome do próximo arquivo: {arquivo_nc_nome}\n")

                # Gera o caminho completo do arquivo .nc
                arquivo_nc_caminho = paths.CAMINHO_DADOS_NC / arquivo_nc_nome

                # Verifica se o arquivo já existe
                # Se existir, pula o download
                if arquivo_existe(arquivo_nc_caminho):
                    print(f" -> -> -> Arquivo {arquivo_nc_caminho} já existe. Pulando download.")
                    requisicao_atual += 1
                    porcentagem_cumprida = progresso_requisicao(n_requisicoes, requisicao_atual)
                    print(f" -> -> -> Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)\n")
                    continue

                # O arquivo não existindo, faz a requisição
                requisicao_dados(arquivo_nc_caminho, variavel, ano, pressao_nivel, meses, dias, utc_horas, area, data_format, download_format)

                print(f" -> -> -> Arquivo {arquivo_nc_nome} baixado com sucesso")
                requisicao_atual += 1
                porcentagem_cumprida = progresso_requisicao(n_requisicoes, requisicao_atual)
                print(f" -> -> -> Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)")

    print(f"\n -> -> -> Todos os arquivos .nc foram baixados com sucesso.")


def requisicao_todos_dados_padrao():
    """Requisita todos os dados padrão definidos em ParametrosObtencaoDados."""

    requisicao_multiplos_dados()


# Funções auxiliares
# ----------------------------

def progresso_requisicao(n_requisicoes, requisicao_atual):
    porcentagem_cumprida = round(100 * requisicao_atual/n_requisicoes, 2)
    return porcentagem_cumprida

def arquivo_existe(arquivo_nc_caminho: Path):
    """Verifica se o arquivo existe no caminho especificado."""
    return arquivo_nc_caminho.exists()

def nome_arquivo(variavel, ano, pressao_nivel):
    """Gera o nome do arquivo .nc baseado na variável, ano e nível de pressão."""
    return f"(var-{variavel})_(anos-{ano})_(pressao-{pressao_nivel}).nc"

def calcula_combinacoes(variaveis: tuple, anos: tuple, pressao_niveis: tuple):
    """Calcula o número total de combinações de variáveis, anos e níveis de pressão."""
    return len(variaveis) * len(anos) * len(pressao_niveis)