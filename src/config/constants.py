import numpy as np
from utils.espaco_para_underline import espaco_para_underline
from utils.indice_mais_um import lista_indice_mais_um


class ParametrosObtencaoDados:
    """Define os parâmetros fixos para a obtenção de dados meteorológicos do Climate Data Store.
    
    Attributes:
        VARIAVEIS (tuple): Variáveis meteorológicas a serem requisitadas.
        PRESSAO_NIVEIS (tuple): Níveis de pressão (em hPa) a serem utilizados.
        ANOS, MESES, DIAS, HORAS (tuple): Intervalos temporais considerados.
        AREA (tuple): Coordenadas da Bacia de Campos (norte, oeste, sul, leste).
        DATA_FORMAT (str): Formato dos dados requisitados (ex: 'netcdf').
        DOWNLOAD_FORMAT (str): Formato de download (ex: 'unarchived').
    """

    VARIAVEIS = ("u_component_of_wind", "v_component_of_wind", 
                 "relative_humidity", "temperature", "geopotential") 


    PRESSAO_NIVEIS =  (900, 925, 950, 975, 1000) # Em hPa

    # Parâmetros temporais
    ANOS = tuple(range(2015, 2025))  # (2015 - 2024)
    MESES = tuple(range(1, 13)) 
    DIAS = tuple(range(1, 32)) 
    HORAS = tuple(f"{h:02d}:00" for h in range(24)) 


    # Área

    # Coordenadas da Bacia de Campos
    NORTE = -21.0 # Latitude
    SUL = -24.0 # Latitude
    OESTE = -42.0 # Longitude
    LESTE = -39.0 # Longitude

    AREA = (NORTE, OESTE, SUL, LESTE)

    DATA_FORMAT = 'netcdf'
    DOWNLOAD_FORMAT = 'unarchived'





class ConstantesNumericas:
    """Agrupa constantes numéricas importantes
    
    Attributes:
        G (float): Aceleração da gravidade (m/s²).
    """

    G = 9.80665 # Aceleração da gravidade(m/s**2)





class ArquivosNomes:
    """Agrupa nomes de arquivos e padrões de nomes de arquivos.
    
    Attributes:
        PADRAO_ARQUIVOS_NC_ORIGINAIS (str): Padrão geral de nome para os arquivos .nc obtidos do Climate Data Store.
        PADRAO_ARQUIVOS_NC_ORIGINAIS_REGEX (str): Expressão regular para capturar os parâmetros dos nomes dos arquivos netCDF.
        ARQUIVO_NC_UNIDO (str): Nome do arquivo gerado pela união dos datasets originais.
        ARQUIVO_NC_PONTO_NAO_PLATAFORMA (str): Nome do arquivo do dataset gerado para um ponto específico que não é uma plataforma."""

    PADRAO_ARQUIVOS_NC_ORIGINAIS = "(var-*)_(ano-*)_(pressao-*).nc" 
    # O * serve como um wildcard para capturar qualquer sequência de caracteres, 
    # no caso os valores das variáveis armazenados no arquivo
    # Exemplo de nome de arquivo: "var-velocidade_u_ano-2020_pressao-900.nc"


    PADRAO_ARQUIVOS_NC_ORIGINAIS_REGEX = r"\(var-(.+?)\)_\(ano-(\d{4})\)_\(pressao-(\d+?)\).nc" 
    # Explicação da expressão regular:
    # - \(var-(.+?)\): Captura a variável entre parênteses,
    # - \(ano-(\d{4})\): Captura o ano de 4 dígitos entre parênteses,
    # - \(pressao-(\d+?)\): Captura o nível de pressão entre parênteses.
    # - O ponto de interrogação após o quantificador torna a captura não gananciosa, pegando o menor número possível de caracteres.
    # - A barra invertida antes dos parênteses é necessária para escapar os parênteses, pois eles têm significado especial em expressões regulares. 
    
    ARQUIVO_NC_UNIDO = "dataset_unido.nc"

    ARQUIVO_NC_PONTO_NAO_PLATAFORMA = "ponto_nao_plataforma.nc"





class PastasNomes:
    """Agrupa nomes de pastas.

    Attributes:
        DADOS (str): Nome da pasta onde todos os dados serão armazenados.
        DATASETS (str): Nome da pasta onde os datasets serão armazenados.
        DATAFRAMES (str): Nome da pasta onde os dataframes serão armazenados.
        ORIGINAIS (str): Nome da pasta onde os arquivos originais serão armazenados.
        UNIDO (str): Nome da pasta onde o dataset unificado será armazenado.
        COORDENADAS_ESPECIFICAS (str): Nome da pasta onde os dados de coordenadas específicas serão armazenados.
        PLATAFORMAS (str): Nome da pasta onde os dados das plataformas serão armazenados.
        PONTOS_NAO_PLATAFORMA (str): Nome da pasta onde os dados de pontos que não são plataformas serão armazenados.
        TESTES (str): Nome da pasta onde os testes serão armazenados.
        DADOS_GERADOS_TESTES (str): Nome da pasta onde os dados gerados para testes serão armazenados.
    """

    DADOS = "data"
    DATASETS = "datasets"
    DATAFRAMES = "dataframes"
    ORIGINAIS = "originais"
    UNIDO = "unido"
    COORDENADAS_ESPECIFICAS = "coordenadas_especificas"
    PLATAFORMAS = "plataformas"
    PONTOS_NAO_PLATAFORMA = "ponto_nao_plataforma"   

    TESTES = "tests"
    DADOS_GERADOS_TESTES = "dados_gerados_testes"


class FormatosArquivo:
    """Agrupa formatos de arquivo.

    Attributes:
        NETCDF (str): Formato NetCDF.
        PARQUET (str): Formato Parquet.
        FORMATOS_ACEITOS (list): Lista de formatos aceitos.
    """

    NETCDF = "netcdf"
    PARQUET = "parquet"

    FORMATOS_ACEITOS = [NETCDF, PARQUET]



class Correspondencias:
    """Agrupa diversas correspondências de constantes e nomes de variáveis.

    Attributes:
        DadosVariaveis (class): Agrupamento de nomes de variáveis e dimensões para facilitar o acesso e manipulação dos dados obtidos.
        Chaves (class): Agrupamento de chaves utilizadas em dicionários para facilitar o acesso aos dados das plataformas.
    """

    class DadosVariaveis:
        """Agrupa nomes de variáveis e dimensões para facilitar o acesso e manipulação dos dados obtidos.
        
        Attributes:
            VARIAVEIS_REPRESENTACAO_ORIGINAL (dict): Correspondências entre os nomes utilizados para requisitar os dados e os utilizados nos arquivos NetCDF obtidos.
            TEMPO_UTC0 (str): Nome da variável de tempo em UTC.
            TEMPO_BRAS (str): Nome da variável de tempo em horário brasileiro.
            PRESSAO (str): Nome da variável de pressão.
            LATITUDE (str): Nome da variável de latitude.
            LONGITUDE (str): Nome da variável de longitude.
            VELOCIDADE_U (str): Nome da variável de velocidade u.
            VELOCIDADE_V (str): Nome da variável de velocidade v.
            VELOCIDADE_RESULTANTE (str): Nome da variável de velocidade resultante.
            GEOPOTENCIAL (str): Nome da variável de geopotencial.
            ALTURA (str): Nome da variável de altura.
            UMIDADE_RELATIVA (str): Nome da variável de umidade relativa.
            TEMPERATURA_KELVIN (str): Nome da variável de temperatura em Kelvin.
            TEMPERATURA_CELSIUS (str): Nome da variável de temperatura em Celsius.
            ANO (str): Nome da variável de ano.
            MES (str): Nome da variável de mês.
            MES_STR (str): Nome da variável de nome do mês.
            DIA (str): Nome da variável de dia.
            HORA (int): Nome da variável de hora.
            HORA_STR (str): Nome da variável em string de hora.
            NUMBER (str): Nome da variável de número.
            EXP_VER (str): Nome da variável de versão experimental.
            ESTACAO_DO_ANO (str): Nome da variável de estação do ano.
            NOVOS_NOMES (dict): Correspondência entre nomes de variáveis e dimensões antigos, no formato {nome_antigo: nome_novo}.
            NOVA_ORDEM_COLUNAS (list): Lista que define a ordem das colunas dos dataframes gerados.
            NUMERO_PARA_MES (dict): Correspondência entre o número do mês e seu nome
            """
        

        VARIAVEIS_REPRESENTACAO_ORIGINAL = {"u_component_of_wind": "u", "v_component_of_wind": "v", "relative_humidity": "r", 
                                "temperature": "t", "geopotential": "z"}


        # Estes nomes são utilizados para renomear as variáveis e dimensões dos dados obtidos, entre outras coisas,
        # facilitando a manipulação e análise dos dados.
        TEMPO_UTC0 = "tempo_UTC0"
        TEMPO_BRAS = "tempo_bras"
        PRESSAO = "pressao"
        LATITUDE = "lat"
        LONGITUDE = "lon"
        VELOCIDADE_U = "vel_u"
        VELOCIDADE_V = "vel_v"
        VELOCIDADE_RESULTANTE = "vel_res"
        GEOPOTENCIAL = "z"
        ALTURA = "h"
        UMIDADE_RELATIVA = "r"
        TEMPERATURA_KELVIN = "t_K"
        TEMPERATURA_CELSIUS = "t_C"
        ANO = "ano"
        MES = "mes"
        MES_STR = "mes_nome"
        DIA = "dia"
        HORA = "hora"
        HORA_STR = "hora_str"
        NUMBER = "number"
        EXP_VER = "expver"
        ESTACAO_DO_ANO = "estacao"

        # Nem todos os nomes são necessariamente alterados.
        NOVOS_NOMES = {"valid_time": TEMPO_UTC0, 
                    "z": GEOPOTENCIAL, "r": UMIDADE_RELATIVA, 
                    "t": TEMPERATURA_KELVIN, "u": VELOCIDADE_U, 
                    "v": VELOCIDADE_V, "altura": ALTURA}
        

        # Os nomes de colunas foram ordenados de forma a priorizar as variáveis mais importantes para análise como colunas iniciais.
        NOVA_ORDEM_COLUNAS = [ANO, ESTACAO_DO_ANO, MES_STR, 
                              DIA, HORA_STR, ALTURA, VELOCIDADE_U, 
                              VELOCIDADE_V, VELOCIDADE_RESULTANTE, 
                              TEMPERATURA_CELSIUS, TEMPERATURA_KELVIN,  
                              UMIDADE_RELATIVA, GEOPOTENCIAL, TEMPO_BRAS, 
                              MES, HORA, TEMPO_UTC0]
    
   
        NUMERO_PARA_MES = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }


    class Chaves:
        """Agrupa chaves utilizadas em dicionários para facilitar o acesso aos dados das plataformas.
        
        Attributes:
            SIMBOLO_CHAVE (str): Chave para o símbolo da plataforma.
            COORDENADAS_CHAVE (str): Chave para as coordenadas da plataforma.
            ARQUIVO_NC_CHAVE (str): Chave para o nome do arquivo NetCDF
            PASTA_DASK_CHAVE (str): Chave para o nome da pasta no Dask onde os dados da plataforma serão armazenados."""



        SIMBOLO_CHAVE = "simbolo"
        COORDENADAS_CHAVE = "coords"
        ARQUIVO_NC_CHAVE = "arquivo_nc_nome"
        PASTA_DASK_DATAFRAME_CHAVE = "pasta_dask_nome"
    

class OutrasConstantes:
    """Agrupa outras constantes importantes.
    
    Attributes:
        ESTACAO_DO_ANO_DATAS (dict): Datas aproximadas de início e fim das estações do ano.
        ALTURAS_DESEJADAS (np.ndarray): Alturas desejadas para interpolação, de 130 a 350 metros, com passo de 10 metros.
    """

    ALTURAS_DESEJADAS = np.arange(130, 351, 10)

    # As datas reais variam por um ou 2 dias de ano em ano.
    ESTACAO_DO_ANO_DATAS = {"Verão": 
                                {"inicio": 
                                    {"dia": 21, "mes": 12},
                                "fim":
                                    {"dia": 20, "mes": 3}
                                },
                            "Outono": 
                                {"inicio": 
                                    {"dia": 21, "mes": 3},
                                "fim":
                                    {"dia": 20, "mes": 6}
                                },
                            "Inverno": 
                                {"inicio": 
                                    {"dia": 21, "mes": 6},
                                "fim":
                                    {"dia": 22, "mes": 9}
                                },
                            "Primavera": 
                                {"inicio": 
                                    {"dia": 23, "mes": 9},
                                "fim":
                                    {"dia": 20, "mes": 12}
                                }
                            }




class Plataformas:
    """Agrupa dados das plataformas de petróleo na Bacia de Campos
    
    Attributes:
        PLATAFORMAS (list): Nomes das plataformas.
        COORDENADAS (list): Coordenadas das plataformas.
        SIMBOLOS (list): Símbolos das plataformas.

            Exemples: ["p1", "p2", "p3", ...]
        
        ARQUIVOS_NOMES_BASE (list): Base dos nomes dos arquivos para cada plataforma, utilizando o símbolo e o nome da plataforma.

            Exemples: ["p1-NAMORADO_2_(PNA-2)", "p2-PETROBRAS_26_(P-26)", ...]

        ARQUIVOS_NC_NOMES (list): Nomes dos arquivos NetCDF correspondentes, com extensão ".nc".

            Exemples: ["p1-NAMORADO_2_(PNA-2).nc", "p2-PETROBRAS_26_(P-26).nc", ...]

        PASTAS_DASK_DATAFRAME_NOMES (list): Nomes das pastas onde os dados serão armazenados no Dask DataFrame, sem extensão.

            Exemples: ["p1-NAMORADO_2_(PNA-2)", "p2-PETROBRAS_26_(P-26)", ...]

        DADOS (dict): Dados das plataformas, no formato {plataforma: {chave: valor}, onde valor é um dicionário de simbolos, coordenadas, nome do arquivo NetCDF e nome da pasta do arquivo dask dataframe.
        """


    # Nome das plataformas, coordenadas e símbolos correspondentes.
    PLATAFORMAS = ["NAMORADO 2 (PNA-2)", 
                   "PETROBRAS 26 (P-26)", "PETROBRAS 32 (P-32)", 
                   "PETROBRAS 37 (P-37)", "PETROBRAS IX", 
                   "PETROBRAS XIX", "PETROBRAS XXXIII", 
                   "VERMELHO 1 (PVM-1)", "VERMELHO 2 (PVM-2)"]
    
    
    COORDENADAS = [(-22.45073, -40.41175), (-22.4684, -40.02869), 
                   (-22.2051, -40.1431), (-22.4868, -40.09779),
                   (-22.57358, -40.82192), (-22.3927, -40.05438),
                   (-22.37, -40.0267), (-22.16065, -40.27872),
                   (-22.17535, -40.29147)]
    

    # O objetivo é criar uma lista de símbolos que serão utilizados para identificar as plataformas de forma única.
    SIMBOLOS = ["p" + str(indice) for indice in lista_indice_mais_um(PLATAFORMAS)]

    # O nome do arquivo segue o padrão "p1-NAMORADO_2_(PNA-2)", onde "p1" é o símbolo da plataforma e "NAMORADO_2_(PNA-2)" é o nome da plataforma com espaços substituídos por underlines.
    ARQUIVOS_NOMES_BASE = [s + "-" + espaco_para_underline(p) for s, p in zip(SIMBOLOS, PLATAFORMAS)]

    ARQUIVOS_NC_NOMES = [n + ".nc" for n in ARQUIVOS_NOMES_BASE]
    PASTAS_DASK_DATAFRAME_NOMES = ARQUIVOS_NOMES_BASE # Não possui extensão, pois é o nome da pasta onde os dados serão armazenados no Dask.



    DADOS = {
                        p : {
                            Correspondencias.Chaves.SIMBOLO_CHAVE : s, 
                            Correspondencias.Chaves.COORDENADAS_CHAVE : c, 
                            Correspondencias.Chaves.ARQUIVO_NC_CHAVE : na_nc, 
                            Correspondencias.Chaves.PASTA_DASK_DATAFRAME_CHAVE : na_pq
                            } 
                        for s, p, c, na_nc, na_pq in zip(
                            SIMBOLOS, 
                            PLATAFORMAS, 
                            COORDENADAS, 
                            ARQUIVOS_NC_NOMES, 
                            PASTAS_DASK_DATAFRAME_NOMES
                            )   
                        }





if "__main__" == __name__:
    
    # Verificação 
    
    print(f"Anos: {ParametrosObtencaoDados.ANOS} \n")

    print(f"Meses: {ParametrosObtencaoDados.MESES} \n")

    print(f"Dias: {ParametrosObtencaoDados.DIAS} \n")

    print(f"Horas: {ParametrosObtencaoDados.HORAS} \n")

    print(f"Área: {ParametrosObtencaoDados.AREA} \n")

    print(f"Dados das plataformas: {Plataformas.DADOS}")

    print(f"Formato netcdf: {FormatosArquivo.NETCDF}")

