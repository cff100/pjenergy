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
    def obtem_chave(formato_arquivo: Literal["netcdf", "parquet"]) -> str:
        """Decide a chave para o nome do arquivo ou pasta, a partir do formato do arquivo.
            
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar.
        
        Returns:
            str: Nome da chave para o nome do arquivo ou pasta
            Exemples: "arquivo_nc_nome", "pasta_dask_nome"

        """

        if formato_arquivo == fa.NETCDF:
            chave_arquivo_nome = cr.Chaves.ARQUIVO_NC_CHAVE
        elif formato_arquivo == fa.PARQUET:
            chave_arquivo_nome = cr.Chaves.PASTA_DASK_DATAFRAME_CHAVE

        return chave_arquivo_nome
    

    @staticmethod
    def obtem_dados_pasta_nome(formato_arquivo: Literal["netcdf", "parquet"]) -> str:
        """Decide o nome da pasta onde se localizam os arquivos do formato especificado.
            
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar.
        
        Returns:
            str: Nome da pasta de dados
        """

        if formato_arquivo == fa.NETCDF:
            dado_pasta_nome = pn.DATASETS
        elif formato_arquivo == fa.PARQUET:
            dado_pasta_nome = pn.DATAFRAMES

        return dado_pasta_nome


    
    @staticmethod
    def obtem_caminho_relativo(chave_arquivo_nome: str, formato_arquivo: Literal["netcdf", "parquet"], plataforma: Optional[str] = None):
        # EM ANDAMENTO
        # Caso seja escolhida uma plataforma específica
        if plataforma in Plataformas.PLATAFORMAS:
            nome = Plataformas.DADOS[plataforma][chave_arquivo_nome]
            pasta_local = Path(pn.PLATAFORMAS) # Pasta que indica o tipo de local dos dados (platafora ou não plataforma)
        # Caso seja escolhido um outro ponto qualquer coberto pelos dados
        elif plataforma is None:
            pasta_local = Path(pn.PONTOS_NAO_PLATAFORMA)
            if formato_arquivo == fa.NETCDF:
                nome = an.ARQUIVO_NC_PONTO_NAO_PLATAFORMA
            elif formato_arquivo == fa.PARQUET:
                nome = pn.PONTOS_NAO_PLATAFORMA # É na verdade uma pasta
        else:
            raise ValueError(f" {plataforma} é um valor não válido para plataforma. Valores válidos: \n{Plataformas.PLATAFORMAS} \nOu seus simbolos correspondentes: \n{Plataformas.SIMBOLOS}")
        
        # Caminho relativo em relação
        caminho_relativo = pasta_local / nome

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

        chave_arquivo_nome = PathsDados.obtem_chave(formato_arquivo)
        dados_pasta_nome = PathsDados.obtem_dados_pasta_nome(formato_arquivo)

        caminho_relativo = PathsDados.obtem_caminho_relativo(chave_arquivo_nome, formato_arquivo, plataforma)
        
        diretorio_coordenadas_especificas = DiretoriosBasicos.DIRETORIO_DADOS / dados_pasta_nome / pn.COORDENADAS_ESPECIFICAS
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
    #caminho = PathsDados.obter_path_coord_especifica("parquet", "PETROBRAS 26 (P-26)")
    caminho = PathsDados.obter_path_coord_especifica("parquet", "p3")
    print(caminho)