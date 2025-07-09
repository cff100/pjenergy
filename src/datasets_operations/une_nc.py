import re
import glob
from pathlib import Path
import xarray as xr
# Módulos internos do projeto
from config.paths import DIRETORIO_DATASETS_ORIGINAIS, CAMINHO_ABSOLUTO_DATASET_UNIDO
from config.constants import ArquivosNomes as an
from datasets_operations.salva_dataset import salva_dataset_nc

# FUNÇÕES AUXILIARES

def pega_arquivos(diretorio: Path = DIRETORIO_DATASETS_ORIGINAIS) -> list[str]:
    """Pega todos os arquivos de um determinado diretório, com o nome em um determinado padrão"""

    caminho_padrao = str(diretorio) + "\\" + an.PADRAO_ARQUIVOS_NC_ORIGINAIS # Padrão de nome do caminho dos arquivos
    
    # Extrai o nome do padrão para exibir na saída
    nome_padrao = caminho_padrao.split("\\")[-1]

    # Lista todos os arquivos que correspondem ao padrão
    print(f"\nProcurando arquivos com nome no padrão: {nome_padrao} ...\n")
    arquivos = glob.glob(caminho_padrao) 
    print("Arquivos encontrados.\n\n")

    return arquivos


def variaveis_match(arquivo: str) -> tuple[str | None, str | None, str | None]: 
    """Captura informações a partir do nome do arquivo, como variável, ano e nível de pressão."""

    # Utiliza expressão regular para capturar os grupos de interesse do nome dos arquivos que seguem o padrão
    match = re.search(an.PADRAO_ARQUIVOS_NC_ORIGINAIS_REGEX, arquivo) 

    if match:
        variavel, ano, nivel_pressao = match.groups()
        return variavel, ano, nivel_pressao
    else:
        return None, None, None


def constroi_dicio_parametros(diretorio: Path = DIRETORIO_DATASETS_ORIGINAIS) -> dict:
    """
    Dado o diretório, obtém conjuntos dos parâmetros utilizados de variáveis, anos e níveis de pressão.
    Retorna um dicionário aninhado: {variavel: {nivel_pressao: {ano: dataset}}}
    """
    # Obtém os arquivos do diretório que seguem o padrão de nome esperado
    arquivos = pega_arquivos(diretorio)   

    # Cria um dicionário aninhado para armazenar os datasets das combinações de variáveis, anos e níveis de pressão
    print("Organizando datasets em dicionários aninhados...\n")
    dicio_parametros = {}
    for arquivo in arquivos:
        variavel, ano, nivel_pressao = variaveis_match(arquivo) # Captura os parâmetros a partir do nome do arquivo
        if variavel and ano and nivel_pressao:
            ano = int(ano) # Coverte o ano de string para inteiro
            nivel_pressao = int(nivel_pressao) # Converte o nível de pressão de string para inteiro
            # Verifica se a variável, nível de pressão e ano já existem no dicionário
            # Se não existirem, cria as chaves e adiciona o dataset
            if variavel not in dicio_parametros:
                dicio_parametros[variavel] = {}
            if nivel_pressao not in dicio_parametros[variavel]:
                dicio_parametros[variavel][nivel_pressao] = {}
            if ano not in dicio_parametros[variavel][nivel_pressao]:
                dicio_parametros[variavel][nivel_pressao][ano] = xr.open_dataset(arquivo)

    print("Datasets organizados.\n\n")
    return dicio_parametros

# ---------------------------------------------
# FUNÇÕES INTERMEDIÁRIAS (pré-processamento e estruturação de dados)


def concatena_datasets(diretorio: Path = DIRETORIO_DATASETS_ORIGINAIS) -> dict:
    """Concatena os datasets de níveis de pressão e anos diferentes."""

    # Obtém os dicionários de parâmetros, com os datasets das combinações de variáveis, anos e níveis de pressão.
    dicio_parametros = constroi_dicio_parametros(diretorio)

    # Concatena os datasets de anos para cada nível de pressão, e depois concatena os níveis de pressão para cada variável.
    print("Concatenando datasets de diversos níveis de pressão e anos...\n")
    for chave_variavel in dicio_parametros.keys():
        lista_dataset_pressoes = []
        for chave_pressao in sorted(dicio_parametros[chave_variavel].keys()): # Ordena os níveis de pressão em ordem crescente
            lista_dataset_anos = []
            for chave_ano in dicio_parametros[chave_variavel][chave_pressao].keys():
                dataset_anos = dicio_parametros[chave_variavel][chave_pressao][chave_ano]
                lista_dataset_anos.append(dataset_anos)

            # Concatena os datasets de anos para cada nível de pressão
            dataset_pressoes = xr.concat(
                lista_dataset_anos, 
                dim = "valid_time")
            lista_dataset_pressoes.append(dataset_pressoes)

        # Concatena os datasets de diferentes níveis de pressão ao longo da dimensão "pressure_level".
        dicio_parametros[chave_variavel] = xr.concat(
            lista_dataset_pressoes,
            dim="pressure_level")

    print("Concatenação finalizada.\n\n")
    return dicio_parametros


def merge_datasets(dicio_parametros: dict) -> xr.Dataset:
    """Uni os datasets de variáveis dentro de um dicionário aninhado,
    onde as chaves são as variáveis, os níveis de pressão e os anos."""

    # Faz uma lista dos datasets de variáveis
    datasets_variaveis = list(dicio_parametros.values())

    # Concatena os datasets de variáveis em um único dataset
    print("Unindo datasets de todas as variáveis...\n")
    dataset_unico = xr.merge(datasets_variaveis)
    print("Finalizado.\n")
    print(f"Dataset único gerado com {len(dataset_unico.data_vars)} variáveis e {len(dataset_unico.pressure_level)} níveis de pressão.\n\n")
    
    return dataset_unico


# ---------------------------------------------
# FUNÇÃO PRINCIPAL

def unifica_datasets(diretorio_datasets_originais: Path = DIRETORIO_DATASETS_ORIGINAIS, 
                     diretorio_dataset_unido: Path = CAMINHO_ABSOLUTO_DATASET_UNIDO) -> xr.Dataset:
    "Gera um dataset único a partir da combinação dos vários datasets originais."

    # Concatena os datasets de níveis de pressão e anos diferentes
    dicio_parametros = concatena_datasets(diretorio_datasets_originais)

    # Une os datasets de todas variáveis
    dataset_unico = merge_datasets(dicio_parametros)

    # Salva o dataset em um arquivo NetCDF único
    salva_dataset_nc(dataset_unico, diretorio_dataset_unido)

    return dataset_unico


if __name__ == "__main__":
    dataset_unico = unifica_datasets()
    print(dataset_unico)