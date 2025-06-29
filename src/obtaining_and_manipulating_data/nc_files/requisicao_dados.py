
"""Para obtenção de dados de um dataset do Climate Data Store"""
import cdsapi
import config.paths as paths
from pathlib import Path
# Módulos internos do projeto
from config.constants import ParametrosObtencaoDados as pod
from utils.cria_caminho_arquivo import cria_caminho_arquivo


# FUNÇÕES AUXILIARES

def gera_porcentagem_progresso(n_total: int, n_atual: int) -> float:
    """Calcula a porcentagem de progresso de um conjunto de processos."""
    """Parâmetros:
    n_total: Número total de processos.
    n_atual: Número atual de processos concluídos."""

    porcentagem_cumprida = round(100 * n_atual/n_total, 2)
    return porcentagem_cumprida

def gera_nome_arquivo_nc(variavel: str, ano: int, pressao_nivel: int) -> str:
    """Gera o nome do arquivo .nc baseado na variável, ano e nível de pressão."""
    return f"(var-{variavel})_(anos-{ano})_(pressao-{pressao_nivel}).nc" # Essa formatação é importante para manter a consistência e facilitar a identificação dos arquivos baixados.

def calcula_combinacoes(variaveis: tuple, anos: tuple, pressao_niveis: tuple) -> int:
    """Calcula o número total de combinações de variáveis, anos e níveis de pressão."""
    return len(variaveis) * len(anos) * len(pressao_niveis)


# FUNÇÕES PRINCIPAIS

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


def requisicao_multiplos_dados(
                            caminho_base: Path = paths.CAMINHO_DADOS_NC,
                            variaveis: tuple[str, ...] = pod.variaveis, 
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

                arquivo_nc_nome = gera_nome_arquivo_nc(variavel, ano, pressao_nivel)
                print(f"\n -> -> -> Nome do próximo arquivo: {arquivo_nc_nome}\n")

                # Gera o caminho completo do arquivo .nc. 
                # Se o caminho base do arquivo não for especificado, usa o padrão
                arquivo_nc_caminho = cria_caminho_arquivo(arquivo_nc_nome, caminho_base)

                # Verifica se o arquivo já existe
                # Se existir, pula o download
                if arquivo_nc_caminho.exists():
                    print(f" -> -> -> Arquivo {arquivo_nc_caminho} já existe. Pulando download.")
                    requisicao_atual += 1
                    porcentagem_cumprida = gera_porcentagem_progresso(n_requisicoes, requisicao_atual)
                    print(f" -> -> -> Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)\n")
                    continue

                # O arquivo não existindo, faz a requisição
                requisicao_dados(arquivo_nc_caminho, variavel, ano, pressao_nivel, meses, dias, utc_horas, area, data_format, download_format)

                print(f" -> -> -> Arquivo {arquivo_nc_nome} baixado com sucesso")
                requisicao_atual += 1
                porcentagem_cumprida = gera_porcentagem_progresso(n_requisicoes, requisicao_atual)
                print(f" -> -> -> Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)")

    print(f"\n -> -> -> Todos os arquivos .nc foram baixados com sucesso.")


def requisicao_todos_dados_padrao():
    """Requisita todos os dados padrão definidos em ParametrosObtencaoDados."""

    requisicao_multiplos_dados()


