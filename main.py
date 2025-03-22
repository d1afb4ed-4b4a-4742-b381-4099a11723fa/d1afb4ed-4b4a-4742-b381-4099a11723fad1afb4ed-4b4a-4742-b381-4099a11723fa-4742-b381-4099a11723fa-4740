from utils import (
    is_dia_util,
    sortear_horario_entrada,
    sortear_intervalo_almoco,
    calcular_jornada_completa,
    setup_logger,
)
from config import HORARIO_ENTRADA_MIN, HORARIO_ENTRADA_MAX
from ponto import bater_ponto
import datetime
import time

logger = setup_logger()

fake_data = datetime.date(2024, 3, 25)

if not is_dia_util(fake_data):
    logger.info("Hoje não é dia útil (simulado). Nada será feito.")
else:
    entrada_time = sortear_horario_entrada(HORARIO_ENTRADA_MIN, HORARIO_ENTRADA_MAX)
    intervalo = sortear_intervalo_almoco()
    jornada = calcular_jornada_completa(entrada_time, intervalo, fake_data)

    logger.info(
        f"🕒 Jornada sorteada:"
        f"\n  Entrada às {jornada['entrada'].strftime('%H:%M')}"
        f"\n  Saída para almoço às {jornada['saida_almoco'].strftime('%H:%M')}"
        f"\n  Volta do almoço às {jornada['volta_almoco'].strftime('%H:%M')}"
        f"\n  Saída final às {jornada['saida_final'].strftime('%H:%M')}"
        f"\n  Intervalo de almoço: {intervalo.seconds // 60} minutos"
    )

    for etapa, horario in jornada.items():
        if etapa == "intervalo":
            continue

        agora = datetime.datetime.combine(
            datetime.date(2024, 3, 25),
            datetime.datetime.strptime("08:44", "%H:%M").time(),
        )

        segundos_ate_bater = (horario - agora).total_seconds()

        print(agora, horario, segundos_ate_bater)

        if segundos_ate_bater > 0:
            logger.info(
                f"Aguardando {int(segundos_ate_bater // 60)} min para bater ponto de '{etapa}'..."
            )
            time.sleep(segundos_ate_bater)

        logger.info(
            f"Bater ponto: {etapa.upper()} às {datetime.datetime.now().strftime('%H:%M')}"
        )
        bater_ponto(logger)
        logger.info(f"Ponto de '{etapa}' batido com sucesso!")
