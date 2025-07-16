from pathlib import Path
from typing import Optional, Literal

from config.constants import ArquivosNomes as an, PastasNomes as pn, Plataformas, Correspondencias as cr, FormatosArquivo as fa
from utils.gerencia_plataformas_representacoes import gerencia_plataforma_representacoes



class DiretoriosBasicos:
    """Agrupa diretorios básicos do projeto
    
    Attributes:
        DIRETORIO_BASE_GERAL (Path): Diretório base do projeto.
        DIRETORIO_DADOS (Path): Diretório onde se localizam os dados.
        DIRETORIO_TESTES (Path): Diretório onde se localizam os testes.
        """

    # Diretório do projeto
    DIRETORIO_BASE_GERAL = Path(__file__).parent.parent.parent 

    # Diretório da pasta de dados
    DIRETORIO_DADOS = DIRETORIO_BASE_GERAL / pn.DADOS

    # Diretório da pasta de testes
    DIRETORIO_TESTES = DIRETORIO_BASE_GERAL / pn.TESTES  




class PathsDados:
    """Agrupa diretórios principais e fornece funções para construir caminhos para diferentes tipos de dados."""

    @staticmethod
    def obtem_chave_e_nome_pasta(formato_arquivo: Literal["netcdf", "parquet"]) -> tuple[str, str]:
        """Decide a chave para o nome do arquivo ou pasta, a partir do formato do arquivo, 
        além de decidir o nome da pasta onde se localizam os arquivos desse formato específico.
        
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar.
        """

        if formato_arquivo == fa.NETCDF:
            chave = cr.Chaves.SIMBOLO_CHAVE
            pasta_data = pn.DATASETS
        elif formato_arquivo == fa.PARQUET:
            chave = cr.Chaves.SIMBOLO_CHAVE
            pasta_data = pn.DATAFRAMES  
        # else:
        #     raise ValueError(f"Chave não aceita. Valores aceitos: {fa.FORMATOS_ACEITOS}.")
        
        return chave, pasta_data
    
    @staticmethod
    def obtem_caminho_relativo(chave: str, formato_arquivo: Literal["netcdf", "parquet"], plataforma: Optional[str] = None):

        # Caso a plataforma exista na base de dados
        if plataforma in Plataformas.PLATAFORMAS:
            nome_arquivo = Plataformas.DADOS[plataforma][chave]
            caminho_relativo = Path(pn.PLATAFORMAS) / nome_arquivo
        # Caso seja escolhido um outro ponto qualquer coberto pelos dados
        elif plataforma is None:
            if formato_arquivo == fa.NETCDF:
                nome_arquivo = an.ARQUIVO_NC_PONTO_NAO_PLATAFORMA
            elif formato_arquivo == fa.PARQUET:
                nome_arquivo = pn.PONTOS_NAO_PLATAFORMA # É na verdade uma pasta
            caminho_relativo = Path(pn.PONTOS_NAO_PLATAFORMA) / nome_arquivo
        else:
            raise ValueError(f" {plataforma} é um valor não válido para plataforma. Valores válidos: \n{Plataformas.PLATAFORMAS} \nOu seus simbolos correspondentes: \n{Plataformas.SIMBOLOS}")
        
        return caminho_relativo

    @staticmethod
    def obter_path_coord_especifica(formato_arquivo: Literal["netcdf", "parquet"], plataforma: Optional[str] = None) -> Path:   
        """Decide o path (caminho ou diretório) absoluto do arquivo ou pasta que contém dados 
        para coordenadas específicas para uma plataforma, dado o formato de arquivo com o qual 
        se deseja trabalhar.
        
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar. 
                Se `formato_arquivo` for "netcdf", o caminho retornado é de um **arquivo único**. 
                Se for "parquet", o caminho retornado é de uma **pasta** com múltiplos arquivos .parquet.
                
            plataforma (Optional[str]): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.

        Returns: 
            Path: Caminho ou diretório absoluto do arquivo ou pasta.

        """


        if isinstance(plataforma, str): # Condição para descartar os casos em que não é passado nenhuma disciplina em específico (None)
            # Garante a possibilidade de receber tanto o nome completo da plataforma quanto seu símbolo
            plataforma = gerencia_plataforma_representacoes(plataforma)

        chave, pasta_data = PathsDados.obtem_chave_e_nome_pasta(formato_arquivo)

        caminho_relativo = PathsDados.obtem_caminho_relativo(chave, formato_arquivo, plataforma)
        
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
        DIRETORIO_UNIDO = BASE / pn.UNIDO
        CAMINHO_UNIDO = DIRETORIO_UNIDO / an.ARQUIVO_NC_UNIDO

        # Diretório de datasets modificados para representar coordenadas específicas
        DIRETORIO_COORDENADAS_ESPECIFICAS = BASE / pn.COORDENADAS_ESPECIFICAS
        DIRETORIO_PLATAFORMAS = DIRETORIO_COORDENADAS_ESPECIFICAS / pn.PLATAFORMAS
        DIRETORIO_NAO_PLATAFORMAS = DIRETORIO_COORDENADAS_ESPECIFICAS / pn.PONTOS_NAO_PLATAFORMA

    
    class Dataframes:
        """Agrupamento de diretórios e caminhos da pastas onde se localizam dataframes."""

        # Diretório onde se encontram todos os dataframes
        BASE = DiretoriosBasicos.DIRETORIO_DADOS /  pn.DATAFRAMES

        # Diretório de dataframes que representam coordenadas específicas
        DIRETORIO_COORDENADAS_ESPECIFICAS = BASE / pn.COORDENADAS_ESPECIFICAS
        DIRETORIO_PLATAFORMAS = DIRETORIO_COORDENADAS_ESPECIFICAS / pn.PLATAFORMAS
        DIRETORIO_NAO_PLATAFORMAS = DIRETORIO_COORDENADAS_ESPECIFICAS / pn.PONTOS_NAO_PLATAFORMA



    class DadosTeste:

        # Diretório de arquivos criados em testes
        DIRETORIO_DADOS_GERADOS_TESTES = DiretoriosBasicos.DIRETORIO_TESTES / pn.DADOS_GERADOS_TESTES




if __name__ == "__main__":
    caminho = PathsDados.obter_path_coord_especifica("parquet", None)
    print(caminho)