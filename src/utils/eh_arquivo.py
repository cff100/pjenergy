from pathlib import Path

def eh_path_arquivo(caminho: Path) -> None:
    """Verifica se o caminho dado é de um arquivo."""

    if not caminho.is_file():
        raise TypeError(f"O caminho... \n -> {caminho} \n...não é de um arquivo")