
"""Para obtenção  de dados de um dataset do Climate Data Store"""
from config.constants import ParametrosObtencaoDados as pod
import cdsapi
import config.paths as paths

def requisicao_dados(nome_arquivo_nc, variaveis, anos, pressao_niveis, meses = pod.meses, dias = pod.dias, utc_horas = pod.horas, area = pod.area, data_format = pod.data_format, download_format = pod.download_format):

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


def requisicao_todos_dados():

    for variavel in pod.variaveis:
        for ano in pod.anos:
            for pressao_nivel in pod.pressao_niveis:
                arquivo_nc_nome = f"(var-{variavel})_(anos-{ano})_(pressao-{pressao_nivel}).nc"
                arquivo_nc_caminho = paths.CAMINHO_DADOS_NC / arquivo_nc_nome
                requisicao_dados(arquivo_nc_caminho, variavel, ano, pressao_nivel)