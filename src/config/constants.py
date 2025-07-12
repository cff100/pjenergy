from utils.espaco_para_underline import espaco_para_underline
from utils.indice_mais_um import lista_indice_mais_um


class ParametrosObtencaoDados:
    """Agrupamento dos parâmetros utilizados para obtenção dos dados do Climate Data Store"""

    VARIAVEIS = ("u_component_of_wind", "v_component_of_wind", 
                 "relative_humidity", "temperature", "geopotential") 


    PRESSAO_NIVEIS =  (900, 925, 950, 975, 1000) # Em hPa

    # Parâmetros temporais
    ANOS = tuple(range(2015, 2025))  # (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024)
    MESES = tuple(range(1, 13)) # Todos os meses
    DIAS = tuple(range(1, 32)) # Todos os dias
    HORAS = tuple(f"{h:02d}:00" for h in range(24)) # Todas as horas

    #Área

    # Coordenadas da Bacia de Campos
    NORTE = -21.0 # Latitude
    SUL = -24.0 # Latitude
    OESTE = -42.0 # Longitude
    LESTE = -39.0 # Longitude

    AREA = (NORTE, OESTE, SUL, LESTE)

    DATA_FORMAT = 'netcdf'
    DOWNLOAD_FORMAT = 'unarchived'





class ConstantesNumericas:
    """Agrupamento de constantes numéricas importantes"""

    G = 9.80665 # (m/s**2)





class ArquivosNomes:
    """Agrupamentos de nomes de arquivos"""

    # Padrão geral de nome dos arquivos .nc obtidos do Climate Data Store
    PADRAO_ARQUIVOS_NC_ORIGINAIS = "(var-*)_(anos-*)_(pressao-*).nc" 
    # O * serve como um wildcard para capturar qualquer sequência de caracteres, 
    # no caso os valores das variáveis armazenados no arquivo

    # Regex para capturar os parâmetros dos nomes dos arquivos .nc
    PADRAO_ARQUIVOS_NC_ORIGINAIS_REGEX = r"\(var-(.+?)\)_\(anos-(\d{4})\)_\(pressao-(\d+?)\).nc" 
    # Explicação da expressão regular:
    # - \(var-(.+?)\): Captura a variável entre parênteses,
    # - \(anos-(\d{4})\): Captura o ano de 4 dígitos entre parênteses,
    # - \(pressao-(\d+?)\): Captura o nível de pressão entre parênteses.
    # - O ponto de interrogação após o quantificador torna a captura não gananciosa, pegando o menor número possível de caracteres.
    # - A barra invertida antes dos parênteses é necessária para escapar os parênteses, pois eles têm significado especial em expressões regulares. 
    
    # Nome do arquivo gerado pela união dos datasets originais
    ARQUIVO_NC_UNIDO = "dataset_unido.nc"

    # Nome do arquivo do dataset gerado para um ponto específico que não é uma plataforma
    ARQUIVO_NC_PONTO_NAO_PLATAFORMA = "pontos_nao_plataforma.nc"





class PastasNomes:
    """Agrupamento de nomes de pastas"""

    DADOS = "data"
    DATASETS = "datasets"
    DATAFRAMES = "dataframes"
    ORIGINAIS = "originais"
    UNIDO = "unido"
    COORDENADAS_ESPECIFICAS = "coordenadas_especificas"
    PLATAFORMAS = "plataformas"
    PONTOS_NAO_PLATAFORMA = "pontos_nao_plataforma"   

    TESTES = "tests"
    DADOS_GERADOS_TESTES = "dados_gerados_testes"

class FormatosArquivo:
    NETCDF = "netcdf"
    PARQUET = "parquet"
    DASK = "dask"

    FORMATOS_ACEITOS = [NETCDF, PARQUET, DASK]



class Correspondencias:
    
    # --------------------------------------------------------------------
    # Agrupamento de nomes de colunas e variáveis para facilitar o acesso

    # Dicionário de correspondências entre os nomes utilizados para requisitar os dados e os utilizados nos arquivos NetCDF obtidos.
    VARIAVEIS_REPRESENTACAO_ORIGINAL = {"u_component_of_wind": "u", "v_component_of_wind": "v", "relative_humidity": "r", 
                               "temperature": "t", "geopotential": "z"}

    # Conjunto de novos nomes de variáveis e dimensões
    # Estes nomes são utilizados para renomear as variáveis e dimensões dos dados obtidos,
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
    MES_NOME = "mes_nome"
    DIA = "dia"
    HORA = "hora"
    NUMBER = "number"
    EXP_VER = "expver"
    ESTACAO_DO_ANO = "estacao"

    # Dicionário {nome pré-existente : novo nome}. Associa um novo nome aos nomes de variáveis e dimensões. 
    # Nem todos os nomes são necessariamente alterados.
    NOVOS_NOMES = {"valid_time": TEMPO_UTC0, "pressure_level": PRESSAO, 
                   "z": GEOPOTENCIAL, "r": UMIDADE_RELATIVA, 
                   "t": TEMPERATURA_KELVIN, "u": VELOCIDADE_U, 
                   "v": VELOCIDADE_V}
    
    # # Lista da ordem das colunas finais do dataframe
    # lista_colunas_ordem = [ano, estacao_do_ano, mes_nome, mes, dia, hora, pressao, geopotencial, 
    #                  altura, latitude, longitude, velocidade_u, velocidade_v, 
    #                  velocidade_resultante, temperatura_kelvin, temperatura_celsius, 
    #                  umidade_relativa, tempo_UTC0, tempo_bras]


    # ----------------------------------------------------------------------
    # Chaves do dicionário das plataformas
    SIMBOLO_CHAVE = "simbolo"
    COORDENADAS_CHAVE = "coords"
    ARQUIVO_NC_CHAVE = "arquivo_nc_nome"
    PASTA_DASK_CHAVE = "pasta_dask_nome"
    




class OutrasConstantes:
    """Agrupamento de outras constantes importantes"""

    # Dicionário de correspondência entre o número do mês e seu nome
    NUMERO_PARA_MES = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }


    # Dicionário com as datas aproximadas de início e fim das estações do ano.
    # OBS: As datas reais variam por um ou 2 dias de ano em ano.
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
    """Agrupamento de dados das plataformas de petróleo na Bacia de Campos"""


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
    

    # Criação de símbolos para as plataformas, começando com "p1", "p2", etc.
    # O objetivo é criar uma lista de símbolos que serão utilizados para identificar as plataformas de forma única.
    SIMBOLOS_PLATAFORMAS = ["p" + str(indice) for indice in lista_indice_mais_um(PLATAFORMAS)]

    # Criação dos nomes dos arquivos para cada plataforma, utilizando o símbolo e o nome da plataforma.
    # O nome do arquivo segue o padrão "p1-NAMORADO_2_(PNA-2)", onde "p1" é o símbolo da plataforma e "NAMORADO_2_(PNA-2)" é o nome da plataforma com espaços substituídos por underlines.
    ARQUIVO_PLATAFORMAS_NOME = [s + "-" + espaco_para_underline(p) for s, p in zip(SIMBOLOS_PLATAFORMAS, PLATAFORMAS)]

    ARQUIVO_NC_PLATAFORMAS_NOME = [n + ".nc" for n in ARQUIVO_PLATAFORMAS_NOME]
    PASTA_DASK_PLATAFORMAS_NOME = ARQUIVO_PLATAFORMAS_NOME # Não possui extensão, pois é o nome da pasta onde os dados serão armazenados no Dask.



    PLATAFORMAS_DADOS = {
                        p : {
                            Correspondencias.SIMBOLO_CHAVE : s, 
                            Correspondencias.COORDENADAS_CHAVE : c, 
                            Correspondencias.ARQUIVO_NC_CHAVE : na_nc, 
                            Correspondencias.PASTA_DASK_CHAVE : na_pq
                            } 
                        for s, p, c, na_nc, na_pq in zip(
                            SIMBOLOS_PLATAFORMAS, 
                            PLATAFORMAS, 
                            COORDENADAS, 
                            ARQUIVO_NC_PLATAFORMAS_NOME, 
                            PASTA_DASK_PLATAFORMAS_NOME
                            )   
                        }





if "__main__" == __name__:
    
    print(f"Anos: {ParametrosObtencaoDados.ANOS} \n")

    print(f"Meses: {ParametrosObtencaoDados.MESES} \n")

    print(f"Dias: {ParametrosObtencaoDados.DIAS} \n")

    print(f"Horas: {ParametrosObtencaoDados.HORAS} \n")

    print(f"Área: {ParametrosObtencaoDados.AREA} \n")

    print(f"Dados das plataformas: {Plataformas.PLATAFORMAS_DADOS}")

    print(f"Formato netcdf: {FormatosArquivo.NETCDF}")

