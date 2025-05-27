from config.constants import Constantes
from datetime import datetime, timedelta

def brasilia_para_utc(brasilia_horario: str) -> str :
    "Converte o horário de Brasília para o UTC (Universal Time Coordinated)."

    # Converter a string em um objeto datetime
    brasilia_horario = datetime.strptime(brasilia_horario, "%H:%M")
    # Calcular o UTC pela soma da variação dos fusos horários
    utc_horario = brasilia_horario + timedelta(hours=3)
    # Retornar o objeto datetime à uma string
    utc_horario = utc_horario.strftime("%H:%M")

    return utc_horario



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
    utc_hora = brasilia_para_utc("04:00")
    print(utc_hora)
