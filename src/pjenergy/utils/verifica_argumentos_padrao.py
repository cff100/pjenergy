
def erro_algum_parametro_diferente_do_padrao(parametros_lista: list, mensagem_erro: str, valor_padrao: str = "padrao"):
    """Levanta um erro caso algum dos parâmetros passados em lista seja diferente do valor padrão.
    
    Args:
        parametros_lista (list): Lista dos parâmetros a serem analisados.
        mensagem_erro (str): Mensagem de erro a ser exibido, no caso do `valor_padrao` não ser atendido.
        valor_padrao (str): Valor padrão que se busca atender
    
    Raises:
        ValueError: Erro caso algum dos parâmetros fuja do valor padrão
    """
    
    if any(elem != valor_padrao for elem in parametros_lista):
        raise ValueError(mensagem_erro)

def erro_algum_parametro_igual_ao_padrao(parametros_lista: list, mensagem_erro: str, valor_padrao: str = "padrao"):
    """Levanta um erro caso algum dos parâmetros passados em lista seja igual do valor padrão.

    Args:
        parametros_lista (list): Lista dos parâmetros a serem analisados.
        mensagem_erro (str): Mensagem de erro a ser exibido, no caso do `valor_padrao` ser atendido.
        valor_padrao (str): Valor padrão que se busca não atender
    
    Raises:
        ValueError: Erro caso algum dos parâmetros fuja do valor padrão   
    """

    if any(elem == valor_padrao for elem in parametros_lista):
        raise ValueError(mensagem_erro)
    