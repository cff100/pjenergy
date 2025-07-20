
def representa_progresso(indice_atual: int, itens_lista: list) -> str:
    """Retorna a string que representa o progresso de um processo de contagem de itens.
    
    Args:
        indice_atual (int): Indice atual.
        itens_lista (lista): Lista de itens que serão contados.

    Returns:
        str: String do progresso, no formato 'indice_atual/total'.
    """

    return f"{indice_atual}/{len(itens_lista)}"