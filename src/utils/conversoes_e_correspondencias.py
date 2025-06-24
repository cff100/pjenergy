from config.constants import Constantes
from datetime import datetime, timedelta

def utc_para_brasilia(utc_horario: str) -> str :
    "Converte o horário de UTC (Universal Time Coordinated) para o de Brasília."

    # Converter a string em um objeto datetime
    utc_horario_dt = datetime.strptime(utc_horario, "%H:%M")
    # Calcular o UTC pela soma da variação dos fusos horários
    brasilia_horario = utc_horario_dt - timedelta(hours=3)
    # Retornar o objeto datetime à uma string
    brasilia_horario = brasilia_horario.strftime("%H:%M")

    return brasilia_horario



def calcula_altura_geopotencial(geopotencial: float) -> int:
    """Calcula o valor da altura a partir do valor obtido para o geopotencial,
    para assim poder realizar a correspondência entre pressão e altura."""

    h = geopotencial / Constantes.g
    return h

def calcula_altura_atm_padrao():
    pass


if "__main__" == __name__:
    h = calcula_altura_geopotencial(10)
    print(h)
    utc_hora = utc_para_brasilia("04:00")
    print(utc_hora)
