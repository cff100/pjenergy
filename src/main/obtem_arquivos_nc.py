from obtaining_data import data_request

def baixa_arquivos_nc():
    """Função para baixar os arquivos .nc do Climate Data Store (CDS)"""

    data_request.requisicao_todos_dados()


if __name__ == "__main__":
    baixa_arquivos_nc()
    