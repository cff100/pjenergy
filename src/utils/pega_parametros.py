import re
from typing import Optional
import glob
from config.paths import CAMINHO_DADOS_NC
from pathlib import Path


def pega_parametros(diretorio: Path = CAMINHO_DADOS_NC) -> tuple[list, list, list]:
    """Dado o diretório, obtém conjuntos dos parâmetros utilizados de variáveis, anos e níveis de pressão."""

    arquivos = pega_arquivos(diretorio)   

    variaveis_conjunto = set()
    anos_conjunto = set()
    niveis_pressao_conjunto = set()
    for arquivo in arquivos:
        match = match_nome_padrao(arquivo)
        if match:
            variavel, ano, nivel_pressao = match.groups()
            variaveis_conjunto.add(variavel) 
            anos_conjunto.add(int(ano))
            niveis_pressao_conjunto.add(int(nivel_pressao))

    variaveis = sorted(variaveis_conjunto)
    anos = sorted(anos_conjunto)
    niveis_pressao = sorted(niveis_pressao_conjunto)

    return variaveis, anos, niveis_pressao


def pega_arquivos(diretorio: Path = CAMINHO_DADOS_NC) -> list[str]:
    """Pega todos os arquivos de um determinado diretório, com o nome em um determinado padrão"""

    padrao = str(diretorio) + "\\(var-*)_(anos-*)_(pressao-*).nc"
    nome_padrao = padrao.split("\\")[-1]
    print(f"Procurando arquivos no padrão, com nome: {nome_padrao}\n")
    arquivos = glob.glob(padrao)

    return arquivos


def match_nome_padrao(arquivo: str) -> Optional[re.Match]: 
    """Verifica se o nome do arquivo segue o padrão esperado e retorna os grupos correspondentes."""
    match = re.search(r"\(var-(.+?)\)_\(anos-(\d{4})\)_\(pressao-(\d+?)\)", arquivo)
    return match


if __name__ == "__main__":
    #arquivos = pega_arquivos()
    variaveis, anos, niveis_pressao = pega_parametros()
    print(f"Variáveis: {variaveis}")
    print(f"Anos: {anos}")
    print(f"Níveis de Pressão: {niveis_pressao}")