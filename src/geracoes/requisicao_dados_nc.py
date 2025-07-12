
"""Para obtenção de dados de um dataset do Climate Data Store"""

import cdsapi
from pathlib import Path
# Módulos internos do projeto
from config.paths import PathsDados as pad
from config.constants import ParametrosObtencaoDados as pod



# FUNÇÕES AUXILIARES

def gera_porcentagem_progresso(n_total: int, n_atual: int) -> float:
    """Calcula a porcentagem de progresso de um conjunto de processos."""
    """Parâmetros:
    n_total: Número total de processos.
    n_atual: Número atual de processos concluídos."""

    porcentagem_cumprida = round(100 * n_atual/n_total, 2)
    return porcentagem_cumprida

def gera_nome_arquivo_nc_padrao(variavel: str, ano: int, pressao_nivel: int) -> str:
    """Gera o nome do arquivo .nc baseado na variável, ano e nível de pressão."""
    return f"(var-{variavel})_(anos-{ano})_(pressao-{pressao_nivel}).nc" 
# ATENÇÃO!!
# Essa formatação do nome do arquivo é muito importante para manter a consistência 
# e facilitar a identificação dos arquivos baixados.
# Não é recomendado, mas tenha certeza do que está fazendo se for alterar.

def calcula_combinacoes(variaveis: tuple, anos: tuple, pressao_niveis: tuple) -> int:
    """Calcula o número total de combinações de variáveis, anos e níveis de pressão."""
    return len(variaveis) * len(anos) * len(pressao_niveis)



# FUNÇÕES PRINCIPAIS

# def requisicao_dados(
#                     variavel: str, # Apenas uma variável por vez, como 'u_component_of_wind'
#                     ano: int, # Apenas um ano por vez, como 2020
#                     pressao_nivel: int,  # Apenas um nível de pressão por vez, como 900
#                     meses: tuple[int, ...] = pod.MESES, 
#                     dias: tuple[int, ...] = pod.DIAS, 
#                     utc_horas: tuple[str, ...] = pod.HORAS, 
#                     area: tuple[float, float, float, float] = pod.AREA, 
#                     data_format: str = pod.DATA_FORMAT, 
#                     download_format: str = pod.DOWNLOAD_FORMAT,
#                     arquivo_nome: str = "padrao",
#                     datasets_diretorio: Path = pad.Datasets.DIRETORIO_ORIGINAIS,
#                     substituir: bool = False) -> None: 
#     """Requisita dados do Climate Data Store (CDS) e salva em um arquivo NetCDF.
#     Parâmetros:
#     - datasets_diretorio: diretório da pasta onde o arquivo será salvo.
#     - substituir: True para substituir o arquivo com o mesmo nome caso já exista."""

#     # Criar diretório dos diretórios, caso ainda não exista
#     if not datasets_diretorio.exists():
#         datasets_diretorio.mkdir(parents=True, exist_ok=True)
#         print(f" -> -> -> Diretório '{datasets_diretorio}' criado com sucesso.")

#     if arquivo_nome == "padrao":
#         arquivo_nome = gera_nome_arquivo_nc(variavel, ano, pressao_nivel)
#     print(f"\n -> -> -> Nome do arquivo atual: {arquivo_nome}\n")
    
#     dataset_caminho = datasets_diretorio / arquivo_nome

#     if dataset_caminho.exists() and substituir == False:
#         raise FileExistsError(f"\n -> -> -> Erro: O arquivo {arquivo_nome} já existe. " \
#             "Para substituí-lo, mude o parâmetro 'substituir' para True."
#         )
#     else:
#         print("\nIniciando requisição... (Tempo médio: 12 minutos).\n")

#     # Inicializar API do CDS
#     c = cdsapi.Client() # Exige que o url e a key já estejam configurados em um arquivo .cdsapirc externo.
    
#     # Requisição dos dados
#     dataset = 'reanalysis-era5-pressure-levels'
#     request = {
#     'product_type': ['reanalysis'],
#     'variable': variavel,
#     'year': ano,
#     'month': meses,
#     'day': dias,
#     'time': utc_horas,
#     'area': area,  
#     'pressure_level': pressao_nivel,  # Em hPa
#     'data_format': data_format,
#     'download_format': download_format
#     }

#     c.retrieve(dataset, request, dataset_caminho)

#     print(f"Requisição de {arquivo_nome} concluída com sucesso!")


# def requisicao_multiplos_dados(
#                             variaveis: tuple[str, ...] = pod.VARIAVEIS, 
#                             anos: tuple[int, ...] = pod.ANOS, 
#                             pressao_niveis: tuple[int, ...] = pod.PRESSAO_NIVEIS, 
#                             meses: tuple[int, ...] = pod.MESES, 
#                             dias: tuple[int, ...] = pod.DIAS, 
#                             utc_horas: tuple[str, ...] = pod.HORAS, 
#                             area: tuple[float, float, float, float] = pod.AREA, 
#                             data_format: str = pod.DATA_FORMAT, 
#                             download_format: str = pod.DOWNLOAD_FORMAT,
#                             datasets_diretorio: Path = pad.Datasets.DIRETORIO_ORIGINAIS) -> None:
#     """Faz loops para a obtenção de vários arquivos NetCDF de acordo com os valores passados como parâmetros."""

#     n_requisicoes = calcula_combinacoes(variaveis, anos, pressao_niveis)
#     print(f"\n -> -> -> Número total de requisições: {n_requisicoes}\n")
#     requisicao_atual = 0

#     for variavel in variaveis:
#         for ano in anos:
#             for pressao_nivel in pressao_niveis:

#                 # Monta o caminho do arquivo apenas para verificar sua existência
#                 arquivo_nome = gera_nome_arquivo_nc(variavel, ano, pressao_nivel)
#                 dataset_caminho = datasets_diretorio / arquivo_nome

#                 # Verifica se o arquivo já existe
#                 # Se existir, pula o download
#                 if dataset_caminho.exists():
#                     print(f" -> -> -> Arquivo {dataset_caminho} já existe. Pulando download.")
#                     requisicao_atual += 1
#                     porcentagem_cumprida = gera_porcentagem_progresso(n_requisicoes, requisicao_atual)
#                     print(f" -> -> -> Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)\n")
#                     continue

#                 # O arquivo não existindo, faz a requisição
#                 requisicao_dados(variavel, ano, pressao_nivel, 
#                                  meses, dias, utc_horas, area, 
#                                  data_format, download_format, 
#                                  "padrao", datasets_diretorio) 

#                 requisicao_atual += 1
#                 porcentagem_cumprida = gera_porcentagem_progresso(n_requisicoes, requisicao_atual)
#                 print(f" -> -> -> Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)")

#     print(f"\n -> -> -> Todos os arquivos .nc foram baixados com sucesso.")



# ---------------

def requisicao_dados(
                    dataset_caminho: Path,
                    variavel: str, # Apenas uma variável por vez, como 'u_component_of_wind'
                    ano: int, # Apenas um ano por vez, como 2020
                    pressao_nivel: int,  # Apenas um nível de pressão por vez, como 900
                    meses: tuple[int, ...] = pod.MESES, 
                    dias: tuple[int, ...] = pod.DIAS, 
                    utc_horas: tuple[str, ...] = pod.HORAS, 
                    area: tuple[float, float, float, float] = pod.AREA, 
                    data_format: str = pod.DATA_FORMAT, 
                    download_format: str = pod.DOWNLOAD_FORMAT,
                    substituir: bool = False) -> None: 
    """Requisita dados do Climate Data Store (CDS) e salva em um arquivo NetCDF.
    Parâmetros:
    - substituir: True para substituir o arquivo com o mesmo nome caso já exista."""

    # Criar diretório dos datasets, caso ainda não exista
    datasets_diretorio = dataset_caminho.parent
    if not datasets_diretorio.exists():
        datasets_diretorio.mkdir(parents=True, exist_ok=True)
        print(f" -> -> -> Diretório '{datasets_diretorio}' criado com sucesso.")

    arquivo_nome = dataset_caminho.name
    print(f"\n -> -> -> Nome do arquivo atual: {arquivo_nome}\n")
    
    if dataset_caminho.exists() and substituir == False:
        raise FileExistsError(f"\n -> -> -> Erro: O arquivo {arquivo_nome} já existe. " \
            "Para substituí-lo, mude o parâmetro 'substituir' para True."
        )
    else:
        print("\nIniciando requisição... (Tempo médio: 3 minutos).\n")

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

    c.retrieve(dataset, request, dataset_caminho)

    print(f"Requisição de {arquivo_nome} concluída com sucesso!")


def requisicao_multiplos_dados(
                            variaveis: tuple[str, ...] = pod.VARIAVEIS, 
                            anos: tuple[int, ...] = pod.ANOS, 
                            pressao_niveis: tuple[int, ...] = pod.PRESSAO_NIVEIS, 
                            meses: tuple[int, ...] = pod.MESES, 
                            dias: tuple[int, ...] = pod.DIAS, 
                            utc_horas: tuple[str, ...] = pod.HORAS, 
                            area: tuple[float, float, float, float] = pod.AREA, 
                            data_format: str = pod.DATA_FORMAT, 
                            download_format: str = pod.DOWNLOAD_FORMAT) -> None:
    """Faz loops para a obtenção de vários arquivos NetCDF de acordo com os valores passados como parâmetros.
    O caminho onde os datasets são salvos é fixo."""

    n_requisicoes = calcula_combinacoes(variaveis, anos, pressao_niveis)
    print(f"\n -> -> -> Número total de requisições: {n_requisicoes}\n")
    requisicao_atual = 0

    for variavel in variaveis:
        for ano in anos:
            for pressao_nivel in pressao_niveis:

                # Monta o caminho do arquivo apenas para verificar sua existência
                arquivo_nome = gera_nome_arquivo_nc_padrao(variavel, ano, pressao_nivel)
                dataset_caminho = pad.Datasets.DIRETORIO_ORIGINAIS / arquivo_nome

                # Verifica se o arquivo já existe
                # Se existir, pula o download
                if dataset_caminho.exists():
                    print(f" -> -> -> Arquivo {dataset_caminho} já existe. Pulando download.")
                    requisicao_atual += 1
                    porcentagem_cumprida = gera_porcentagem_progresso(n_requisicoes, requisicao_atual)
                    print(f" -> -> -> Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)\n")
                    continue

                # O arquivo não existindo, faz a requisição
                requisicao_dados(dataset_caminho, variavel, 
                                 ano, pressao_nivel, meses, 
                                 dias, utc_horas, area, 
                                 data_format, download_format) 

                requisicao_atual += 1
                porcentagem_cumprida = gera_porcentagem_progresso(n_requisicoes, requisicao_atual)
                print(f" -> -> -> Progresso atual: {requisicao_atual}/{n_requisicoes} ({porcentagem_cumprida}%)")

    print(f"\n -> -> -> Todos os arquivos .nc foram baixados com sucesso.")