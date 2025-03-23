import os
import json
import datetime
import time

from config import HORARIO_ENTRADA_MIN, HORARIO_ENTRADA_MAX
from ponto import bater_ponto
from utils import (
    is_dia_util,
    sortear_horario_entrada,
    sortear_intervalo_almoco,
    calcular_jornada_completa,
    setup_logger,
)

logger = setup_logger()
data_hoje = datetime.date.today()

hora_utc = datetime.datetime.now(datetime.timezone.utc).hour

etapa_por_hora = {
    0: "entrada",  # 08:00 BRT
    4: "saida_almoco",  # 12:00 BRT
    5: "volta_almoco",  # 13:00 BRT
    9: "saida_final",  # 17:00 BRT
}

logger.info(f"⏰ Hora UTC: {hora_utc}")
logger.info(f"📅 Horário atual: {datetime.datetime.now(datetime.timezone.utc)}")

etapa = etapa_por_hora.get(hora_utc)
if etapa is None:
    logger.warning("⏳ Hora não corresponde a nenhuma etapa. Encerrando.")
    exit(0)

logger.info(f"Etapa detectada automaticamente: {etapa}")

if not is_dia_util(data_hoje):
    logger.info("Hoje não é dia útil. Nada será feito.")
    exit(0)

if etapa == "entrada":
    entrada_time = sortear_horario_entrada(HORARIO_ENTRADA_MIN, HORARIO_ENTRADA_MAX)
    intervalo = sortear_intervalo_almoco()
    jornada = calcular_jornada_completa(entrada_time, intervalo, data_hoje)

    with open("jornada.json", "w") as f:
        json.dump({k: v.strftime("%Y-%m-%d %H:%M:%S") for k, v in jornada.items()}, f)
    logger.info("🧠 Jornada sorteada e salva em jornada.json")
else:
    if not os.path.exists("jornada.json"):
        logger.warning("⚠️ Jornada não encontrada. Nada será feito.")
        exit(0)

    with open("jornada.json", "r") as f:
        jornada = json.load(f)

horario = datetime.datetime.strptime(jornada[etapa], "%Y-%m-%d %H:%M:%S")
delta = (horario - datetime.datetime.now()).total_seconds()

if delta > 0:
    logger.info(f"Aguardando {int(delta // 60)} minutos até a batida de '{etapa}'...")
    time.sleep(delta)

logger.info(
    f"Bater ponto: {etapa.upper()} às {datetime.datetime.now().strftime('%H:%M')}"
)
bater_ponto(logger)
logger.info(f"Ponto de '{etapa}' batido com sucesso!")
