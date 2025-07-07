from config.constants import OutrasConstantes as oc

def gerencia_plataforma_nome(string: str) -> str:
    """Faz com que o nome do símbolo da plataforma seja uma string válida para representá-la, 
    além de levantar um erro se o nome da plataforma for inexistente"""

    plataformas_lista = list(oc.plataformas_dados.keys())

    for plataforma in plataformas_lista:
        if oc.plataformas_dados[plataforma]["simbolo"] == string:
            print(f"\n Plataforma escolhida: {plataforma}\n")
            return plataforma
        else:
            pass

    # Levanta erro caso o nome dado não corresponder à nenhuma plataforma 
    if plataforma not in plataformas_lista:
        raise ValueError("Não existe uma plataforma com este nome no banco de dados.")
    
    return string
        
if __name__ == "__main__":
    plataforma = gerencia_plataforma_nome("PETROBRAS 26 (P-26)")
    print(plataforma)