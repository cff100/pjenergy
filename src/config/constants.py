
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
    norte = -21.0
    sul = -24.0
    oeste = -42.0
    leste = -39.0

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
    
    NOME_PADRAO_ARQUIVO_NC_UNICO = "dataset_unico.nc"


if "__main__" == __name__:
    
    print(f"Anos: {ParametrosObtencaoDados.anos} \n")

    print(f"Meses: {ParametrosObtencaoDados.meses} \n")

    print(f"Dias: {ParametrosObtencaoDados.dias} \n")

    print(f"Horas: {ParametrosObtencaoDados.horas} \n")

    print(f"Área: {ParametrosObtencaoDados.area} \n")

