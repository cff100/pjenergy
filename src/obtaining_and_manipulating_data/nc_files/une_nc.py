import re
import glob
from pathlib import Path
import xarray as xr
# Módulos internos do projeto
from config.paths import CAMINHO_DADOS_NC
from config.constants import ConstantesString as cs

# FUNÇÕES AUXILIARES

def pega_arquivos(diretorio: Path = CAMINHO_DADOS_NC) -> list[str]:
    """Pega todos os arquivos de um determinado diretório, com o nome em um determinado padrão"""

    caminho_padrao = str(diretorio) + "\\" + cs.NOME_PADRAO_ARQUIVOS_NC_GERAL # Padrão de nome do caminho dos arquivos
    # Extrai o nome do padrão para exibir na saída
    nome_padrao = caminho_padrao.split("\\")[-1]
    print(f"\nProcurando arquivos com nome no padrão: {nome_padrao}\n")
    # Lista todos os arquivos que correspondem ao padrão
    arquivos = glob.glob(caminho_padrao) 

    return arquivos


def variaveis_match(arquivo: str) -> tuple[str | None, str | None, str | None]: 
    """Captura informações a partir do nome do arquivo, como variável, ano e nível de pressão."""
    # Utiliza expressão regular para capturar os grupos de interesse do nome dos arquivos que seguem o padrão
    match = re.search(cs.NOME_PADRAO_ARQUIVOS_NC_REGEX, arquivo) 

    if match:
        variavel, ano, nivel_pressao = match.groups()
        return variavel, ano, nivel_pressao
    else:
        return None, None, None

# ---------------------------------------------
# FUNÇÕES INTERMEDIÁRIAS (pré-processamento e estruturação de dados)

def constroi_dicio_parametros(diretorio: Path = CAMINHO_DADOS_NC) -> dict:
    """
    Dado o diretório, obtém conjuntos dos parâmetros utilizados de variáveis, anos e níveis de pressão.
    Retorna um dicionário aninhado: {variavel: {nivel_pressao: {ano: dataset}}}
    """
    # Obtém os arquivos do diretório que seguem o padrão de nome esperado
    arquivos = pega_arquivos(diretorio)   

    # Cria um dicionário aninhado para armazenar os datasets das combinações de variáveis, anos e níveis de pressão
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
    return dicio_parametros

# ---------------------------------------------
# FUNÇÕES PRINCIPAIS

def concatena_datasets(diretorio: Path = CAMINHO_DADOS_NC) -> dict:
    """Concatena os datasets de variáveis por níveis de pressão e anos."""
    # Obtém os dicionárioos de parâmetros, com os datasets das combinações de variáveis, anos e níveis de pressão.
    dicio_parametros = constroi_dicio_parametros(diretorio)
    # Concatena os datasets de anos para cada nível de pressão, e depois concatena os níveis de pressão para cada variável.
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

    return dicio_parametros


def merge_datasets(dicio_parametros: dict) -> xr.Dataset:
    """Uni os datasets de variáveis dentro de um dicionário aninhado,
    onde as chaves são as variáveis, os níveis de pressão e os anos."""

    # Faz uma lista dos datasets de variáveis
    datasets_variaveis = list(dicio_parametros.values())
    # Concatena os datasets de variáveis em um único dataset
    dataset_unico = xr.merge(datasets_variaveis)
    print(f"Dataset único gerado com {len(dataset_unico.data_vars)} variáveis e {len(dataset_unico.pressure_level)} níveis de pressão.")
    
    return dataset_unico


def salva_dataset_unico(dataset: xr.Dataset, nome_arquivo: str = cs.NOME_PADRAO_ARQUIVO_NC_UNICO, diretorio: Path = CAMINHO_DADOS_NC) -> None:
    """Salva o dataset único em um arquivo .nc. 
    Caso o nome do arquivo seja diferente do default, 
    é necessário adicionar o nome do arquivo ao .gitignore na raiz do projeto 
    (sob a sessão de arquivos grandes)."""
    
    caminho_dataset_unico = diretorio / nome_arquivo

    # Garante a extensão correta do arquivo
    if not caminho_dataset_unico.suffix == ".nc":
        caminho_dataset_unico = caminho_dataset_unico.with_suffix(".nc")
    dataset.to_netcdf(caminho_dataset_unico)
    print(f"Dataset único salvo em: {caminho_dataset_unico}")




if __name__ == "__main__":
    dicio_parametros = constroi_dicio_parametros()
    dataset_unico = merge_datasets(dicio_parametros)
    print(dataset_unico)