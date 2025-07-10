from pathlib import Path

def identifica_formato_arquivo(caminho: Path) -> str:
    """Identifica o formato do arquivo pelo sufixo do caminho passado"""

    sufixo = caminho.suffix

    if sufixo == ".nc":
        formato_arquivo = "netcfd"
    elif sufixo == ".parquet":
        formato_arquivo = "parquet"

    return formato_arquivo