from pathlib import Path
from typing import Optional

from config.constants import ArquivosNomes as an, PastasNomes as pn, Plataformas as plt, Correspondencias as cr, FormatosArquivo as fa
from utils.gerencia_plataformas_representacoes import gerencia_plataforma_representacoes



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

    @staticmethod
    def obter_caminho_coord_especifica(formato_arquivo: str, plataforma: Optional[str] = None) -> Path:   
        """Decide o caminho absoluto a partir do valor de 'formato_arquivo' e 'plataforma'.
        \nParâmetros:
        - formato_arquivo: str, deve ser "netcdf" ou "parquet".
        - plataforma: str ou None, se for None, o caminho será para um ponto não específico.
        Retorna:
        - caminho: Path, caminho absoluto do arquivo correspondente.
        """

        # Verifica se o formato do arquivo é string e chama a função de gerência de plataforma
        # para garantir a possibilidade de receber tanto o nome completo da plataforma quanto seu símbolo.
        if isinstance(plataforma, str):
            plataforma = gerencia_plataforma_representacoes(plataforma)

        if formato_arquivo == fa.NETCDF:
            chave = cr.ARQUIVO_NC_CHAVE
            pasta_data = pn.DATASETS
        elif formato_arquivo == fa.PARQUET:
            chave = cr.ARQUIVO_PARQUET_CHAVE
            pasta_data = pn.DATAFRAMES  
        else:
            raise ValueError("Chave não aceita. Valores aceitos: 'netcdf' ou 'parquet'.")
        

        # Caso a plataforma exista na base de dados
        if plataforma in plt.PLATAFORMAS:
            nome_arquivo = plt.PLATAFORMAS_DADOS[plataforma][chave]
            caminho_relativo = Path(pn.PLATAFORMAS) / nome_arquivo
        # Caso seja escolhido um outro ponto qualquer coberto pelos dados
        elif plataforma is None:
            nome_arquivo = an.ARQUIVO_NC_PONTO_NAO_PLATAFORMA
            caminho_relativo = Path(pn.PONTOS_NAO_PLATAFORMA) / nome_arquivo
        else:
            raise ValueError(f"Valor não válido para plataforma. Valores válidos: \n{plt.PLATAFORMAS} \nOu seus simbolos correspondentes: \n{plt.SIMBOLOS_PLATAFORMAS}")
        
        diretorio_coordenadas_especificas = DiretoriosBasicos.DIRETORIO_DADOS / pasta_data / pn.COORDENADAS_ESPECIFICAS
        caminho = diretorio_coordenadas_especificas / caminho_relativo

        return caminho

    class Datasets:
        """Agrupamento de diretórios e caminhos da pastas onde se localizam datasets."""

        # Diretório da pasta onde se encontram todos os datasets
        BASE = DiretoriosBasicos.DIRETORIO_DADOS / pn.DATASETS 

        # Diretório dos arquivos originais obtidos do Climate Data Store
        DIRETORIO_ORIGINAIS = BASE / pn.ORIGINAIS

        # Caminhos relativo e absoluto do arquivo feito da união dos arquivos originais obtidos
        CAMINHO_RELATIVO_UNIDOS = Path(pn.UNIDO) / an.ARQUIVO_NC_UNIDO
        CAMINHO_ABSOLUTO_UNIDOS = BASE / CAMINHO_RELATIVO_UNIDOS 

        # Diretório de datasets modificados para representar coordenadas específicas
        DIRETORIO_COORDENADAS_ESPECIFICAS = BASE / pn.COORDENADAS_ESPECIFICAS

    
    class Dataframes:
        """Agrupamento de diretórios e caminhos da pastas onde se localizam dataframes."""

        # Diretório onde se encontram todos os dataframes
        BASE = DiretoriosBasicos.DIRETORIO_DADOS /  pn.DATAFRAMES

        # Diretório de dataframes que representam coordenadas específicas
        DIRETORIO_COORDENADAS_ESPECIFICAS = BASE / pn.COORDENADAS_ESPECIFICAS


    class DadosTeste:

        # Diretório de arquivos criados em testes
        DIRETORIO_DADOS_GERADOS_TESTES = DiretoriosBasicos.DIRETORIO_TESTES / pn.DADOS_GERADOS_TESTES




if __name__ == "__main__":
    caminho = PathsDados.obter_caminho_coord_especifica("netcdf", "NAMORADO 2 (PNA-2)") # Exemplo de erro na plataforma
    print(caminho)