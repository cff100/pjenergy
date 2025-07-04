import numpy as np
from config.constants import OutrasConstantes as oc

def decide_estacao_vetorizado(dia: int, mes: int) -> np.ndarray:
    "Escolhe a estação no ano de acordo com o dia e mês recebido."

    estacoes_do_ano_lista = list(oc.estacao_do_ano_dados.keys())
    
    # for estacao in estacoes_do_ano_lista:
    #     # Pega os dias e meses de início e fim das estações
    #     dia_inicio = oc.estacao_do_ano_dados[estacao]["inicio"]["dia"]
    #     mes_inicio = oc.estacao_do_ano_dados[estacao]["inicio"]["mes"]
    #     dia_fim = oc.estacao_do_ano_dados[estacao]["fim"]["dia"]
    #     mes_fim = oc.estacao_do_ano_dados[estacao]["fim"]["mes"]

    #     if (mes == mes_inicio and dia >= dia_inicio) or (mes_fim - 2 <= mes <= mes_fim - 1) or (mes == mes_fim and dia <= dia_fim):
    #         return estacao

    condicoes = []
    estacoes = []

    for estacao, limites in oc.estacao_do_ano_dados.items():
        di, mi = limites["inicio"]["dia"], limites["inicio"]["mes"] # Dia e mes inicial da estação
        df, mf = limites["fim"]["dia"], limites["fim"]["mes"] # Dia e mês final da estação

        if mi < mf:
            # Todas estações do ano, exceto Verão
            cond = (
                ((mes == mi) & (dia >= di)) |
                ((mes > mi) & (mes < mf)) |
                ((mes == mf) & (dia <= df))
            )
        else:
            # Apenas Verão
            cond = (
                ((mes == mi) & (dia >= di)) |
                ((mes < mf)) |
                ((mes == mf) & (dia <= df))
            )

        condicoes.append(cond)
        estacoes.append(estacao)

    return np.select(condicoes, estacoes, default="Desconhecida")
        

if __name__ == "__main__":
    # Exemplo
    estacao = decide_estacao_vetorizado(20, 7)
    print(estacao)