from config.constants import Plataformas as plat, Correspondencias as cr

def gerencia_plataforma_representacoes(representacao: str ) -> str:
    """Gerencia a representação de plataformas, convertendo símbolos em nomes de plataformas específicos.

    Parâmetros:
    - representacao: str
    Pode ser um nome padronizado de plataforma, um símbolo associado ou outro valor qualquer. 
    Se for um nome já padronizado ou um valor irreconhecível, será mantido sem alteração.

    Retorna:
    - str: nome da plataforma correspondente ou o próprio valor se não houver conversão.
    """


    # Não altera nada caso a representação não seja algum dos símbolos registrados, mesmo que seja um nome errado da plataforma
    if representacao not in plat.SIMBOLOS_PLATAFORMAS:
        if representacao not in plat.PLATAFORMAS:
            # Aviso para quando a representação não correponde a nenhuma plataforma e nem a nenhum símbolo delas.
            print(f"\nMantido o nome original: {representacao}\n") 
        return representacao

    # Busca o nome da plataforma associada ao símbolo
    for plataforma in plat.PLATAFORMAS:
        if plat.PLATAFORMAS_DADOS[plataforma][cr.SIMBOLO_CHAVE] == representacao:
            print(f"\nCorrespondência: {representacao} -> {plataforma}\n")
            return plataforma
        
    raise ValueError(
        f"Valor de 'representacao' inválido: {representacao}."
        f"Símbolos válidos: {plat.SIMBOLOS_PLATAFORMAS}"
        )

if __name__ == "__main__":
    plataforma = gerencia_plataforma_representacoes("p3")   
    plataforma = gerencia_plataforma_representacoes("PETROBRAS 26 (P-26)")