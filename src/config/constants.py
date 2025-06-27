
class ParametrosObtencaoDados:
    """Agrupamento dos parâmetros utilizados para obtenção dos dados"""

    variaveis = ("u_component_of_wind", "v_component_of_wind", 
                 "relative_humidity", "temperature", "geopotential")

    pressao_niveis =  (900, 925, 950, 975, 1000) # Em hPa

    # Parâmetros temporais
    anos = tuple(range(2015, 2025))  # (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024)
    meses = tuple(range(1, 13)) # Todos os meses
    dias = tuple(range(1, 32)) # Todos os dias
    horas = tuple(f"{h:02d}:00" for h in range(24)) # Todas as horas

    #Área

    # Coordenadas da Bacia de Campos
    norte = -21
    sul = -24
    oeste = -42
    leste = -39

    area = (norte, oeste, sul, leste)

    data_format = 'netcdf'
    download_format = 'unarchived'


class Constantes:

    g = 9.80665 #m/s**2



if "__main__" == __name__:
    
    print(f"Anos: {ParametrosObtencaoDados.anos} \n")

    print(f"Meses: {ParametrosObtencaoDados.meses} \n")

    print(f"Dias: {ParametrosObtencaoDados.dias} \n")

    print(f"Horas: {ParametrosObtencaoDados.horas} \n")

    print(f"Área: {ParametrosObtencaoDados.area} \n")

