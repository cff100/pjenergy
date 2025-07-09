from pathlib import Path
from typing import Optional
from config.constants import ArquivosNomes as an, PastasNomes as pn, Plataformas as plt


class DiretoriosBasicos:
    """Agrupamento dos diretorios básicos do projeto"""

    # Diretório do projeto
    DIRETORIO_BASE_GERAL = Path(__file__).parent.parent.parent 

    # Diretório da pasta de dados
    DIRETORIO_DADOS = DIRETORIO_BASE_GERAL / pn.DADOS

    # Diretório da pasta de testes
    DIRETORIO_TESTES = DIRETORIO_BASE_GERAL / pn.TESTES  


class PathsDados:
    """Agrupamento de diretórios e caminhos da pastas onde se localizam os dados."""

    class Datasets:
        """Agrupamento de diretórios e caminhos da pastas onde se localizam datasets."""

        # Diretório da pasta onde se encontram todos os datasets
        BASE = DiretoriosBasicos.DIRETORIO_DADOS / pn.DATASETS # Diretório da pasta de datasets

        # Diretório da pasta onde se localizam os arquivos originais obtidos do Climate Data Store
        DIRETORIO_ORIGINAIS = BASE / pn.ORIGINAIS

        # Caminho relativo e absoluto do arquivo feito da união dos arquivos originais obtidos
        CAMINHO_RELATIVO_UNIDOS = Path(pn.UNIDO) / an.ARQUIVO_NC_UNIDO
        CAMINHO_ABSOLUTO_UNIDOS = BASE / CAMINHO_RELATIVO_UNIDOS 

        # Diretório de datasets modificados para representar coordenadas específicas
        DIRETORIO_COORDENADAS_ESPECIFICAS = BASE / pn.COORDENADAS_ESPECIFICAS

        @staticmethod
        def decide_caminho_dataset_coordenada_especifica(plataforma: Optional[str] = None) -> Path:
            """Decide o caminho absoluto a partir do valor de 'plataforma'."""

            # Caso a plataforma exista na base de dados
            if plataforma in plt.PLATAFORMAS:
                nome_arquivo = plt.PLATAFORMAS_DADOS[plataforma]["nome_arquivo"]
                caminho_relativo = Path(pn.PLATAFORMAS) / nome_arquivo
            # Caso seja escolhido um outro ponto qualquer coberto pelos dados
            elif plataforma is None:
                nome_arquivo = an.ARQUIVO_NC_PONTO_NAO_PLATAFORMA
                caminho_relativo = Path(pn.PONTOS_NAO_PLATAFORMA) / nome_arquivo
            else:
                raise ValueError("Valor não válido para plataforma")
                

            caminho_absoluto = PathsDados.Datasets.DIRETORIO_COORDENADAS_ESPECIFICAS / caminho_relativo
            
            return caminho_absoluto

# ----------------------

DIRETORIO_DATAFRAMES = DIRETORIO_DADOS / "dataframes" # Diretório de todos os dataframes
DIRETORIO_DATAFRAMES_PLATAFORMAS = DIRETORIO_DATAFRAMES / "plataforms"  # Diretório da pasta com os dataframes de pontos específicos

def caminho_absoluto_dataframe_plataforma(plataforma: str | None) -> Path:
    "Decide o nome do caminho a partir do valor de 'plataforma'. """
    if not plataforma:
        nome_arquivo = "ponto_nao_especifico.parquet"
    else:
        nome_arquivo = oc.plataformas_dados[plataforma]["nome_arquivo"]

    CAMINHO_ABSOLUTO_DATASET_PLATAFORMA = DIRETORIO_DATAFRAMES / "plataforms" / nome_arquivo
    
    return CAMINHO_ABSOLUTO_DATASET_PLATAFORMA

# ----------------------


DIRETORIO_TESTES_ARQUIVOS_NOVOS = DIRETORIO_TESTES / "new_tests_files" # Diretório de arquivos criados em testes
