"""Para baixar arquivos .nc do Climate Data Store (CDS) com configurações específicas diferentes das padrão do projeto.
Útil para testes simplificados ou para obter dados que não estão cobertos pelas configurações padrão do projeto."""

from obtaining_and_manipulating_data import requisicao_dados
# Módulos internos do projeto
from config.paths import CAMINHO_TESTES_ARQUIVOS_NOVOS

# Caminho base para os arquivos .nc a serem baixados. 
# Esse caminho, por padrão, direciona os arquivos baixados para a pasta de arquivos gerados nos testes,
# para evitar conflitos com os arquivos padrão do projeto.
# Se necessário, pode ser alterado para outro caminho, mas atenção para não sobrescrever outros arquivos 
# ou desorganizar a estrutura do projeto.
CAMINHO_BASE = CAMINHO_TESTES_ARQUIVOS_NOVOS

# Exemplo de variáveis, anos, pressões, meses, dias, horas e área não padrão
# Substitua pelos valores reais conforme necessário
VARIAVEIS_NAO_PADRAO = ("geopotential",)     #Ex.: ("u_component_of_wind", "v_component_of_wind", "relative_humidity", "temperature", "geopotential")
ANOS_NAO_PADRAO = (2020,) # Precisar ser uma tupla, mesmo que tenha apenas um ano, como (2022,)
PRESSAO_NIVEIS_NAO_PADRAO = (925,) # Precisar ser uma tupla, mesmo que tenha apenas um nível de pressão, como (950,)
MESES_NAO_PADRAO = (6, 9, 10, 12)
DIAS_NAO_PADRAO = (1, 2, 24, 26, 27, 30, 31)
UTC_HORAS_NAO_PADRAO = ("03:00", "20:00")
AREA_NAO_PADRAO = (-18.0, -45.0, -28.0, -36.0) # Os valores precisam ser float e representam (norte, oeste, sul, leste)
DATA_FORMAT_NAO_PADRAO = "netcdf"  # "netcdf" ou "grib"
DOWNLOAD_FORMAT_NAO_PADRAO = "unarchived" # "unarchived" ou "zip"

def baixa_arquivos_nc_outros():
    """Função para baixar os arquivos .nc do Climate Data Store (CDS), 
    utilizando configurações específicas diferentes das padrão do projeto."""
    requisicao_dados.requisicao_multiplos_dados(caminho_base = CAMINHO_BASE, 
                                                variaveis=VARIAVEIS_NAO_PADRAO, 
                                                anos=ANOS_NAO_PADRAO, 
                                                pressao_niveis=PRESSAO_NIVEIS_NAO_PADRAO, 
                                                meses=MESES_NAO_PADRAO, 
                                                dias=DIAS_NAO_PADRAO, 
                                                utc_horas=UTC_HORAS_NAO_PADRAO, 
                                                area=AREA_NAO_PADRAO, 
                                                data_format=DATA_FORMAT_NAO_PADRAO, 
                                                download_format=DOWNLOAD_FORMAT_NAO_PADRAO)


if __name__ == "__main__":
    baixa_arquivos_nc_outros()