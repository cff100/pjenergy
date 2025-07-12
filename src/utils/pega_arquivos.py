import glob
from pathlib import Path
from config.paths import PathsDados as pad
from config.constants import ArquivosNomes as an


def pega_arquivos(diretorio: Path = pad.Datasets.DIRETORIO_ORIGINAIS, nome_padrao: str = an.PADRAO_ARQUIVOS_NC_ORIGINAIS) -> list[str]:
    """Pega todos os arquivos de um determinado diretório, com o nome em um determinado padrão"""

    caminho_padrao = diretorio / nome_padrao  # Padrão de nome do caminho dos arquivos
    caminho_padrao = str(caminho_padrao)
    
    # Extrai o nome do padrão para exibir na saída
    #nome_padrao = caminho_padrao.split("\\")[-1]

    # Lista todos os arquivos que correspondem ao padrão
    print(f"Procurando arquivos com nome no padrão: {nome_padrao} ...\n")
    arquivos = glob.glob(caminho_padrao) 
    print("Arquivos encontrados.\n\n")

    return arquivos


if __name__ == "__main__":
    arquivos = pega_arquivos()
    print(arquivos)