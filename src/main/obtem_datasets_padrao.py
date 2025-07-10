# Módulos internos do projeto
from geracao.requisicao_dados import requisicao_multiplos_dados

def baixa_arquivos_nc_padrao() -> None:
    """Função para baixar os arquivos .nc do Climate Data Store (CDS), 
    utilizando as configurações padrão do projeto."""

    requisicao_multiplos_dados()


if __name__ == "__main__":
    baixa_arquivos_nc_padrao()
    