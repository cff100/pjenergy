from pathlib import Path

def existe_path(arquivo_caminho: Path) -> None:
    """Verifica a existência de um arquivo ou diretório."""

    if not arquivo_caminho.exists():
        raise FileNotFoundError(f"\nO arquivo... \n -> {arquivo_caminho} \n...não foi encontrado.\n")


if __name__ == "__main__":
    # Exemplo de levantamento de erro
    existe_path(Path("a/b/c/d/e/f"))