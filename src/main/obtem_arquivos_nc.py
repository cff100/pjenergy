from obtaining_data import requisicao_dados

def baixa_arquivos_nc():
    """Função para baixar os arquivos .nc do Climate Data Store (CDS)"""

    requisicao_dados.requisicao_todos_dados_padrao()


if __name__ == "__main__":
    baixa_arquivos_nc()
    