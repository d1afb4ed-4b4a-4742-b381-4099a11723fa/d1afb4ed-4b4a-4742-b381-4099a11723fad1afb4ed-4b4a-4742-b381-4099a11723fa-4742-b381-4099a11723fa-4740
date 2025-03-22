import os
from dotenv import load_dotenv


load_dotenv()


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_DEST = os.getenv("EMAIL_DEST")


LOGIN_USER = os.getenv("LOGIN_USER")
LOGIN_PASS = os.getenv("LOGIN_PASS")


PORTAL_URL = os.getenv("PORTAL_URL")


CHROME_PATH = "/usr/bin/google-chrome"
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"


HORARIO_ENTRADA_MIN = "08:00"
HORARIO_ENTRADA_MAX = "09:00"
JORNADA_HORAS = 8


MODO_SIMULACAO = True
