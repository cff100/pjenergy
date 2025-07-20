
def espaco_para_underline(nome: str) -> str:
    """Muda os espaços de um nome para undeline.
    
    Args:
        nome (str): Nome a ser alterado.

    Returns: 
        str: Nome modificado.
    """

    nome = nome.replace(" ", "_")

    return nome


if __name__ == "__main__":
    # Teste
    nome = espaco_para_underline("casa azul")
    print(nome)