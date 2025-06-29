# Módulos internos do projeto
from obtaining_and_manipulating_data import requisicao_dados

def baixa_arquivos_nc_padrao():
    """Função para baixar os arquivos .nc do Climate Data Store (CDS), 
    utilizando as configurações padrão do projeto."""

    requisicao_dados.requisicao_todos_dados_padrao()


if __name__ == "__main__":
    baixa_arquivos_nc_padrao()
    