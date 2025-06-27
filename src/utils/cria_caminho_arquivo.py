from pathlib import Path

def cria_caminho_arquivo(arquivo_caminho_relativo: Path | str, caminho_base: Path) -> Path:
    """Gera o caminho completo do arquivo .nc baseado no caminho relativo a um caminho base."""

    arquivo_nc = caminho_base / arquivo_caminho_relativo
    return arquivo_nc