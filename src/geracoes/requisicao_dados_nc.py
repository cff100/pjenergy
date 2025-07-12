
"""Para obtenção de dados de um dataset do Climate Data Store"""

from typing import Literal, cast
import cdsapi
from pathlib import Path
# Módulos internos do projeto
from config.paths import PathsDados as pad
from config.constants import ParametrosObtencaoDados as pod
from utils.existencia_path import cria_path_se_nao_existe, verifica_erro_ja_existe_path, existe_path_e_exibe_mensagem
from utils.verifica_argumentos_padrao import erro_algum_parametro_diferente_do_padrao, erro_algum_parametro_igual_ao_padrao



# FUNÇÕES AUXILIARES ----------------------------------------

def gera_porcentagem_progresso(n_total: int, n_atual: int) -> float:
    """Calcula a porcentagem de progresso de um conjunto de processos."""
    """Parâmetros:
    n_total: Número total de processos.
    n_atual: Número atual de processos concluídos."""

    porcentagem_cumprida = round(100 * n_atual/n_total, 2)
    return porcentagem_cumprida



def exibe_progresso(n_atual: int, n_total: int) -> None:
    porcentagem = gera_porcentagem_progresso(n_total, n_atual)
    print(f" -> -> -> Progresso atual: {n_atual}/{n_total} ({porcentagem}%)\n")




def gera_nome_arquivo_nc_padrao(variavel: str, ano: int, pressao_nivel: int) -> str:
    """Gera o nome do arquivo .nc baseado na variável, ano e nível de pressão."""
    return f"(var-{variavel})_(anos-{ano})_(pressao-{pressao_nivel}).nc" 
# ATENÇÃO!!
# Essa formatação do nome do arquivo é muito importante para manter a consistência 
# e facilitar a identificação dos arquivos baixados.
# Não é recomendado, mas tenha certeza do que está fazendo se for alterar.



def calcula_combinacoes(variaveis: tuple, anos: tuple, pressao_niveis: tuple) -> int:
    """Calcula o número total de combinações de variáveis, anos e níveis de pressão."""
    n_requisicoes = len(variaveis) * len(anos) * len(pressao_niveis)
    print(f"\n -> -> -> Número total de requisições: {n_requisicoes}\n")
    return n_requisicoes


def prepara_arquivo_para_download(caminho: Path, substituir: bool = False) -> str:
    """Prepara o diretório do caminho e verifica se o arquivo já existe.
    
    Lança FileExistsError se o arquivo existir e substituir=False.
    """
    diretorio = caminho.parent
    cria_path_se_nao_existe(diretorio)

    nome = caminho.name
    print(f"\n -> -> -> Nome do arquivo atual: {nome}\n")

    if not substituir:
        verifica_erro_ja_existe_path(caminho, f"\n -> -> -> Erro: O arquivo {nome} já existe. \
                                        Para substituí-lo, mude o parâmetro 'substituir' para True.")

    return nome




# FUNÇÕES INTERMEDIÁRIAS ----------------------------------------

def requisita_dados_simples(
                    dataset_salvamento_caminho: Path,
                    variavel: str, # Apenas uma variável por vez, como 'u_component_of_wind'
                    ano: int, # Apenas um ano por vez, como 2020
                    pressao_nivel: int,  # Apenas um nível de pressão por vez, como 900
                    substituir: bool = False) -> None: 
    """Requisita dados do Climate Data Store (CDS) e salva em um arquivo NetCDF.
    Parâmetros:
    - substituir: True para substituir o arquivo com o mesmo nome caso já exista."""

    arquivo_nome = prepara_arquivo_para_download(dataset_salvamento_caminho, substituir)

    # Inicializar API do CDS
    c = cdsapi.Client() # Exige que o url e a key já estejam configurados em um arquivo .cdsapirc externo.
    
    # Requisição dos dados
    dataset = 'reanalysis-era5-pressure-levels'
    request = {
    'product_type': ['reanalysis'],
    'variable': variavel,
    'year': ano,
    'month': pod.MESES,
    'day': pod.DIAS,
    'time': pod.HORAS,
    'area': pod.AREA,  
    'pressure_level': pressao_nivel,  # Em hPa
    'data_format': pod.DATA_FORMAT,
    'download_format': pod.DOWNLOAD_FORMAT
    }

    c.retrieve(dataset, request, dataset_salvamento_caminho)

    print(f"Requisição de {arquivo_nome} concluída com sucesso!")



def requisita_multiplos_dados() -> None:
    
    """Faz loops para a obtenção de vários arquivos NetCDF de acordo com os valores passados como parâmetros.
    O caminho onde os datasets são salvos é fixo."""

    n_requisicoes = calcula_combinacoes(pod.VARIAVEIS, pod.ANOS, pod.PRESSAO_NIVEIS)
    
    requisicao_atual = 0

    for variavel in pod.VARIAVEIS:
        for ano in pod.ANOS:
            for pressao_nivel in pod.PRESSAO_NIVEIS:

                # Monta o caminho do arquivo
                arquivo_nome = gera_nome_arquivo_nc_padrao(variavel, ano, pressao_nivel)
                dataset_salvamento_caminho = pad.Datasets.DIRETORIO_ORIGINAIS / arquivo_nome

                # Verifica se o arquivo já existe
                # Se existir, pula o download
                if existe_path_e_exibe_mensagem(dataset_salvamento_caminho, 
                                                f" -> -> -> Arquivo {dataset_salvamento_caminho} já existe. Pulando download."):
                    requisicao_atual += 1
                    exibe_progresso(requisicao_atual, n_requisicoes)
                    continue

                # O arquivo não existindo, faz a requisição
                requisita_dados_simples(dataset_salvamento_caminho, variavel, ano, pressao_nivel) 

                requisicao_atual += 1
                exibe_progresso(requisicao_atual, n_requisicoes)

    print(f"\n -> -> -> Todos os arquivos .nc foram baixados com sucesso.\n")


# FUNÇÃO PRINCIPAL ----------------------------------------

def requisita_dados_api(
                    usa_multiplos_dados: bool = True,
                    dataset_salvamento_caminho: Path | Literal["padrao"] = "padrao",
                    variavel: str = "padrao", 
                    ano: int | Literal["padrao"] = "padrao", 
                    pressao_nivel: int | Literal["padrao"] = "padrao", 
                    substituir: bool = False) -> None: 
    
    # Monta lista com parametros que tem a possibilidade de receber o valor 'padrao'
    parametros_possivel_padrao = [dataset_salvamento_caminho, variavel, ano, pressao_nivel]

    if usa_multiplos_dados:
        erro_algum_parametro_diferente_do_padrao(parametros_possivel_padrao, 
                                                 "Quando 'usa_multiplos_dados' é True, se pode usar apenas o valor 'padrao' para os parâmetros.")
        requisita_multiplos_dados()

    elif not usa_multiplos_dados:
        erro_algum_parametro_igual_ao_padrao(parametros_possivel_padrao,
                                             "Quando 'usa_multiplos_dados' é False, não se pode usar o valor 'padrao' para nenhum parâmetro.")
            
        requisita_dados_simples(cast(Path, dataset_salvamento_caminho), variavel, cast(int, ano), cast(int, pressao_nivel), substituir)
        # O cast() serve apenas para ajudar o verificador de tipo estático, para os casos em que ele não reconhece o tipo preciso.