from pathlib import Path

def verifica_erro_nao_existe_path(path: Path) -> None:
    """Verifica a existência de um arquivo ou diretório e levanta erro caso não exista."""

    if not path.exists():
        raise FileNotFoundError(f"\nO arquivo... \n -> {path} \n...não existe.\n")


def verifica_erro_ja_existe_path(path: Path, mensagem_erro: str) -> None:

    if path.exists():
        raise FileExistsError(mensagem_erro)


def cria_path_se_nao_existe(path: Path) -> None:

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f" -> -> -> Diretório '{path}' criado com sucesso.")


def existe_path_e_exibe_mensagem(path: Path, mensagem: str) -> bool:

    existe = path.exists()
    if existe:
        print(mensagem)
    return existe


def garante_path_pai_existencia(path: Path) -> None:
    """Cria pastas parentais para um path caso não exista
    
    Args:
        path (Path): Path cujo pastas parentais se busca garantir
    """

    path.parent.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    
    # Testes
    
    verifica_erro_nao_existe_path(Path("a/b/c/d/e/f")) # Exemplo de levantamento de erro