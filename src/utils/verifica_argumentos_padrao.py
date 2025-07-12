
def erro_algum_parametro_diferente_do_padrao(parametros_lista: list, mensagem_erro: str, valor_padrao: str = "padrao"):
    """Levanta um erro caso algum dos parâmetros passados em lista seja diferente do valor padrão."""
    if any(elem != valor_padrao for elem in parametros_lista):
        raise ValueError(mensagem_erro)

def erro_algum_parametro_igual_ao_padrao(parametros_lista: list, mensagem_erro: str, valor_padrao: str = "padrao"):
    """Levanta um erro caso algum dos parâmetros passados em lista seja igual do valor padrão."""
    if any(elem == valor_padrao for elem in parametros_lista):
        raise ValueError(mensagem_erro)
    