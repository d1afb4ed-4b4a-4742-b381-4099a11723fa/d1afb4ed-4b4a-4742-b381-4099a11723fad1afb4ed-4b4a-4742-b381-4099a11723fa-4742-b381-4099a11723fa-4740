import datetime
import random
import logging


def is_dia_util(data=None):
    data = data or datetime.date.today()
    return data.weekday() < 5


def sortear_horario_entrada(min_time_str, max_time_str):
    min_time = datetime.datetime.strptime(min_time_str, "%H:%M").time()
    max_time = datetime.datetime.strptime(max_time_str, "%H:%M").time()

    min_seconds = min_time.hour * 3600 + min_time.minute * 60
    max_seconds = max_time.hour * 3600 + max_time.minute * 60

    sorteado = random.randint(min_seconds, max_seconds)
    horas = sorteado // 3600
    minutos = (sorteado % 3600) // 60
    return datetime.time(horas, minutos)


def sortear_intervalo_almoco(min_min=60, max_min=120):
    minutos = random.randint(min_min, max_min)
    return datetime.timedelta(minutes=minutos)


def calcular_jornada_completa(
    entrada: datetime.time, intervalo: datetime.timedelta, data: datetime.date = None
):
    data = data or datetime.date.today()
    entrada_dt = datetime.datetime.combine(data, entrada)

    saida_almoco = entrada_dt + datetime.timedelta(hours=4)
    volta_almoco = saida_almoco + intervalo
    saida_final = volta_almoco + datetime.timedelta(hours=4)

    return {
        "entrada": entrada_dt,
        "saida_almoco": saida_almoco,
        "volta_almoco": volta_almoco,
        "saida_final": saida_final,
        "intervalo": intervalo,
    }


def calcular_saida(
    entrada: datetime.time, jornada_horas=8, intervalo=datetime.timedelta(hours=1)
):
    entrada_dt = datetime.datetime.combine(datetime.date.today(), entrada)
    saida_dt = entrada_dt + datetime.timedelta(hours=jornada_horas) + intervalo
    return saida_dt.time()


def setup_logger():
    logger = logging.getLogger("ponto_logger")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    fh = logging.FileHandler("logs/ponto.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
