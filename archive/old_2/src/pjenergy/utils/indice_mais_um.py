
def lista_indice_mais_um(elementos: list | tuple) -> list:
    """Cria uma lista de índices a partir de 1 para cada elemento de uma lista ou tupla.
    
    Args:
        elementos (list | tuple): Grupo de elementos dos quais se quer obter os índices.

    Returns:
        list: Lista de índices dos elementos.
    """

    indices = [elementos.index(elemento) + 1 for elemento in elementos]

    return indices


if __name__ == "__main__":

    # EXEMPLO
    indices = lista_indice_mais_um(["A", "B", "C", "D", "E"])
    print(indices)