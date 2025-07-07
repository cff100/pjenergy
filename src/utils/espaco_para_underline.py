
def espaco_para_underline(nome: str) -> str:

    nome = nome.replace(" ", "_")

    return nome


if __name__ == "__main__":
    nome = espaco_para_underline("casa azul")
    print(nome)