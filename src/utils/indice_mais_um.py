
def lista_indice_mais_um(lista: list | tuple) -> list:

    indices = [lista.index(elemento) + 1 for elemento in lista]
    return indices


if __name__ == "__main__":
    indices = lista_indice_mais_um(["A", "B", "C", "D", "E"])
    print(indices)