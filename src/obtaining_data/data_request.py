
"""Para obtenção  de dados de um dataset do Climate Data Store"""
from config.constants import ParametrosObtencaoDados as pod
import cdsapi

def requisicao_dados(nome_arquivo_nc, variaveis, anos, meses, dias, utc_horas, pressao_niveis, area = pod.area, data_format = pod.data_format, download_format = pod.download_format):

    # Inicializar API do CDS
    c = cdsapi.Client() # Exige que o url e a key já estejam configurados em um arquivo .cdsapirc externo.
    
    # Requisição dos dados
    dataset = 'reanalysis-era5-pressure-levels'
    request = {
    'product_type': ['reanalysis'],
    'variable': variaveis,
    'year': anos,
    'month': meses,
    'day': dias,
    'time': utc_horas,
    'area': area,  
    'pressure_level': pressao_niveis,  # Em hPa
    'data_format': data_format,
    'download_format': download_format
    }

    c.retrieve(dataset, request, nome_arquivo_nc)


