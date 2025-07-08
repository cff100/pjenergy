from pathlib import Path

def cria_caminho_arquivo_relativo(arquivo_caminho_relativo: Path | str, diretorio_base: Path) -> Path:
    """Gera o caminho completo de um arquivo baseado no caminho relativo a um diretório base."""

    arquivo = diretorio_base / arquivo_caminho_relativo
    return arquivo