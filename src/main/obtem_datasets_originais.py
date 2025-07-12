from typing import Literal
from pathlib import Path
from geracoes.requisicao_dados_nc import requisita_dados_api

def obtem_datasets_originais(
                    usa_multiplos_dados: bool = True,
                    dataset_salvamento_caminho: Path | Literal["padrao"] = "padrao",
                    variavel: str = "padrao", 
                    ano: int | Literal["padrao"] = "padrao", 
                    pressao_nivel: int | Literal["padrao"] = "padrao", 
                    substituir: bool = False) -> None: 
    """Função para baixar os arquivos netCDF do Climate Data Store (CDS). 
    
    Pode-se baixar arquivos da combinação de argumentos padrão do projeto ou 
    algum arquivo com combinação específica de argumentos únicos (variável, ano e nível de pressão)
    """

    requisita_dados_api(usa_multiplos_dados, dataset_salvamento_caminho, variavel, ano, pressao_nivel, substituir)


if __name__ == "__main__":
    obtem_datasets_originais()
    