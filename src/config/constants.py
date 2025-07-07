from utils.espaco_para_underline import espaco_para_underline
from utils.indice_mais_um import lista_indice_mais_um

class ParametrosObtencaoDados:
    """Agrupamento dos parâmetros utilizados para obtenção dos dados"""

    variaveis = ("u_component_of_wind", "v_component_of_wind", 
                 "relative_humidity", "temperature", "geopotential")  # Representadas respectivamente nos dataset por (u, v, r, t, h)

    pressao_niveis =  (900, 925, 950, 975, 1000) # Em hPa

    # Parâmetros temporais
    anos = tuple(range(2015, 2025))  # (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024)
    meses = tuple(range(1, 13)) # Todos os meses
    dias = tuple(range(1, 32)) # Todos os dias
    horas = tuple(f"{h:02d}:00" for h in range(24)) # Todas as horas

    #Área

    # Coordenadas da Bacia de Campos
    norte = -21.0 # Latitude
    sul = -24.0 # Latitude
    oeste = -42.0 # Longitude
    leste = -39.0 # Longitude

    area = (norte, oeste, sul, leste)

    data_format = 'netcdf'
    download_format = 'unarchived'


class ConstantesNumericas:

    g = 9.80665 #m/s**2


class ConstantesString:
    """Agrupamentos de strings importantes"""

    # Padrão geral de nome dos arquivos .nc
    NOME_PADRAO_ARQUIVOS_NC_GERAL = "(var-*)_(anos-*)_(pressao-*).nc" 
    # O * serve como um wildcard para capturar qualquer sequência de caracteres.

    # Regex para capturar os parâmetros dos nomes dos arquivos .nc
    NOME_PADRAO_ARQUIVOS_NC_REGEX = r"\(var-(.+?)\)_\(anos-(\d{4})\)_\(pressao-(\d+?)\).nc" 
    # Explicação da expressão regular:
    # - \(var-(.+?)\): Captura a variável entre parênteses,
    # - \(anos-(\d{4})\): Captura o ano de 4 dígitos entre parênteses,
    # - \(pressao-(\d+?)\): Captura o nível de pressão entre parênteses.
    # - O ponto de interrogação após o quantificador torna a captura não gananciosa, pegando o menor número possível de caracteres.
    # - A barra invertida antes dos parênteses é necessária para escapar os parênteses, pois eles têm significado especial em expressões regulares. 
    
    NOME_PADRAO_ARQUIVO_NC_UNIDO = "dataset_unido.nc"


class NomeColunasDataframe:

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

    # Dicionário {nome pré-existente : novo nome}. Associa um novo nome aos nomes de colunas vindos do dataframe primário. Nem todos os nomes são necessariamente alterados.
    novos_nomes = {"valid_time": tempo_UTC0, "pressure_level": pressao, 
                   "latitude": latitude, "longitude": longitude, 
                   "z": geopotencial, "r": umidade_relativa, 
                   "t": temperatura_kelvin, "u": velocidade_u, 
                   "v": velocidade_v}
    
    # # Lista da ordem das colunas finais do dataframe
    # lista_colunas_ordem = [ano, estacao_do_ano, mes_nome, mes, dia, hora, pressao, geopotencial, 
    #                  altura, latitude, longitude, velocidade_u, velocidade_v, 
    #                  velocidade_resultante, temperatura_kelvin, temperatura_celsius, 
    #                  umidade_relativa, tempo_UTC0, tempo_bras]


class OutrasConstantes:

    # Dicionário de correspondência entre o número do mês e seu nome
    numero_para_mes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }


    # Dicionário com os dias aproximados de início e fim das estações do ano (os dias reais variam por um ou 2 dias de ano em ano)
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


    # Dados das plataformas
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
    
    simbolos_plataformas = ["p" + str(indice) for indice in lista_indice_mais_um(plataformas)]

    nome_arquivo_plataformas = [s + "-" + espaco_para_underline(p) + ".nc" for s, p in zip(simbolos_plataformas, plataformas)]

    plataformas_dados = {p : {"simbolo" : s, "coords" : c, "nome_arquivo" : na} for s, p, c, na in zip(simbolos_plataformas, plataformas, coordenadas, nome_arquivo_plataformas)}



if "__main__" == __name__:
    
    print(f"Anos: {ParametrosObtencaoDados.anos} \n")

    print(f"Meses: {ParametrosObtencaoDados.meses} \n")

    print(f"Dias: {ParametrosObtencaoDados.dias} \n")

    print(f"Horas: {ParametrosObtencaoDados.horas} \n")

    print(f"Área: {ParametrosObtencaoDados.area} \n")

    print(f"Dados das plataformas: {OutrasConstantes.plataformas_dados}")

