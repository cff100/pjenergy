from utils.espaco_para_underline import espaco_para_underline
from utils.indice_mais_um import lista_indice_mais_um

class ParametrosObtencaoDados:
    """Agrupamento dos parâmetros utilizados para obtenção dos dados"""

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

    g = 9.80665 # (m/s**2) g mantido como letra minúscula pela convensão da representação física.


class ConstantesString:
    """Agrupamentos de strings importantes"""

    # Padrão geral de nome dos arquivos .nc
    NOME_PADRAO_ARQUIVOS_NC_GERAL = "(var-*)_(anos-*)_(pressao-*).nc" 
    # O * serve como um wildcard para capturar qualquer sequência de caracteres, 
    # no caso os valores das variáveis armazenados no arquivo

    # Regex para capturar os parâmetros dos nomes dos arquivos .nc
    NOME_PADRAO_ARQUIVOS_NC_REGEX = r"\(var-(.+?)\)_\(anos-(\d{4})\)_\(pressao-(\d+?)\).nc" 
    # Explicação da expressão regular:
    # - \(var-(.+?)\): Captura a variável entre parênteses,
    # - \(anos-(\d{4})\): Captura o ano de 4 dígitos entre parênteses,
    # - \(pressao-(\d+?)\): Captura o nível de pressão entre parênteses.
    # - O ponto de interrogação após o quantificador torna a captura não gananciosa, pegando o menor número possível de caracteres.
    # - A barra invertida antes dos parênteses é necessária para escapar os parênteses, pois eles têm significado especial em expressões regulares. 
    
    NOME_PADRAO_ARQUIVO_NC_UNIDO = "dataset_unido.nc"


class Correspondencias:
    """Agrupamento de nomes de colunas e variáveis para facilitar o acesso"""

    # Dicionário de correspondências entre os nomes utilizados para requisitar os dados e os utilizados nos arquivos NetCDF obtidos.
    VARIAVEIS_REPRESENTACAO_ORIGINAL = {"u_component_of_wind": "u", "v_component_of_wind": "v", "relative_humidity": "r", 
                               "temperature": "t", "geopotential": "z"}

    # Conjunto de novos nomes de variáveis e dimensões
    # Estes nomes são utilizados para renomear as variáveis e dimensões dos dados obtidos,
    # facilitando a manipulação e análise dos dados.
    tempo_UTC0 = "tempo_UTC0"
    tempo_bras = "tempo_bras"
    pressao = "pressao"
    latitude = "lat"
    longitude = "lon"
    velocidade_u = "vel_u"
    velocidade_v = "vel_v"
    velocidade_resultante = "vel_res"
    geopotencial = "z"
    altura = "h"
    umidade_relativa = "r"
    temperatura_kelvin = "t_K"
    temperatura_celsius = "t_C"
    ano = "ano"
    mes = "mes"
    mes_nome = "mes_nome"
    dia = "dia"
    hora = "hora"
    number = "number"
    exp_ver = "expver"
    estacao_do_ano = "estacao"

    # Dicionário {nome pré-existente : novo nome}. Associa um novo nome aos nomes de variáveis e dimensões. 
    # Nem todos os nomes são necessariamente alterados.
    novos_nomes = {"valid_time": tempo_UTC0, "pressure_level": pressao, 
                   "z": geopotencial, "r": umidade_relativa, 
                   "t": temperatura_kelvin, "u": velocidade_u, 
                   "v": velocidade_v}
    
    # # Lista da ordem das colunas finais do dataframe
    # lista_colunas_ordem = [ano, estacao_do_ano, mes_nome, mes, dia, hora, pressao, geopotencial, 
    #                  altura, latitude, longitude, velocidade_u, velocidade_v, 
    #                  velocidade_resultante, temperatura_kelvin, temperatura_celsius, 
    #                  umidade_relativa, tempo_UTC0, tempo_bras]

    

class OutrasConstantes:
    """Agrupamento de outras constantes importantes"""

    # Dicionário de correspondência entre o número do mês e seu nome
    numero_para_mes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }


    # Dicionário com as datas aproximadas de início e fim das estações do ano.
    # OBS: As datas reais variam por um ou 2 dias de ano em ano.
    estacao_do_ano_dados = {"Verão": 
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
    plataformas = ["NAMORADO 2 (PNA-2)", 
                   "PETROBRAS 26 (P-26)", "PETROBRAS 32 (P-32)", 
                   "PETROBRAS 37 (P-37)", "PETROBRAS IX", 
                   "PETROBRAS XIX", "PETROBRAS XXXIII", 
                   "VERMELHO 1 (PVM-1)", "VERMELHO 2 (PVM-2)"]
    
    
    coordenadas = [(-22.45073, -40.41175), (-22.4684, -40.02869), 
                   (-22.2051, -40.1431), (-22.4868, -40.09779),
                   (-22.57358, -40.82192), (-22.3927, -40.05438),
                   (-22.37, -40.0267), (-22.16065, -40.27872),
                   (-22.17535, -40.29147)]
    
    # Criação de símbolos para as plataformas, começando com "p1", "p2", etc.
    # O objetivo é criar uma lista de símbolos que serão utilizados para identificar as plataformas de forma única.
    simbolos_plataformas = ["p" + str(indice) for indice in lista_indice_mais_um(plataformas)]

    # Criação dos nomes dos arquivos .nc para cada plataforma, utilizando o símbolo e o nome da plataforma.
    # O nome do arquivo segue o padrão "p1-NAMORADO_2_(PNA-2).nc", onde "p1" é o símbolo da plataforma e "NAMORADO_2_(PNA-2)" é o nome da plataforma com espaços substituídos por underlines.
    nome_arquivo_plataformas = [s + "-" + espaco_para_underline(p) + ".nc" for s, p in zip(simbolos_plataformas, plataformas)]

    # Criação de um dicionário que associa cada plataforma a seus dados, incluindo símbolo, coordenadas e nome do arquivo.
    plataformas_dados = {p : {"simbolo" : s, "coords" : c, "nome_arquivo" : na} for s, p, c, na in zip(simbolos_plataformas, plataformas, coordenadas, nome_arquivo_plataformas)}



if "__main__" == __name__:
    
    print(f"Anos: {ParametrosObtencaoDados.ANOS} \n")

    print(f"Meses: {ParametrosObtencaoDados.MESES} \n")

    print(f"Dias: {ParametrosObtencaoDados.DIAS} \n")

    print(f"Horas: {ParametrosObtencaoDados.HORAS} \n")

    print(f"Área: {ParametrosObtencaoDados.AREA} \n")

    print(f"Dados das plataformas: {Plataformas.plataformas_dados}")

