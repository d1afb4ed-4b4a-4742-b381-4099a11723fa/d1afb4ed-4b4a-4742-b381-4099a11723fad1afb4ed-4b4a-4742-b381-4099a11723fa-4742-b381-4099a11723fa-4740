from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import *
import os


def send_email(subject, body):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_DEST
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.sendmail(EMAIL_USER, EMAIL_DEST, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail: {e}")


def bater_ponto(logger):
    logger.info("Iniciando processo de batida de ponto")

    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        logger.info("Abrindo site do ponto...")
        driver.get(PORTAL_URL)
        wait = WebDriverWait(driver, 40)
        logger.info("Site carregado com sucesso.")

        logger.info("Localizando campo de login...")
        user_field = wait.until(EC.presence_of_element_located((By.ID, "login")))
        user_field.send_keys(LOGIN_USER)
        logger.info("Login preenchido.")

        logger.info("Localizando campo de senha...")
        password_field = wait.until(EC.presence_of_element_located((By.ID, "login-pw")))
        password_field.send_keys(LOGIN_PASS)
        logger.info("Senha preenchida.")

        logger.info("Localizando botão de login...")
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_primary"))
        )
        driver.execute_script("arguments[0].click();", login_button)
        logger.info("Botão de login clicado. Aguardando página principal...")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        logger.info("Login realizado com sucesso.")

        logger.info("Localizando botão 'bater ponto'...")
        punch_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-testid='btn_punch_gadget-punch-in']")
            )
        )
        logger.info("Botão 'bater ponto' encontrado.")

        if MODO_SIMULACAO:
            logger.info("🔁 MODO SIMULAÇÃO ATIVO – botão não será clicado.")
        else:
            logger.info("Clicando no botão de ponto...")
            driver.execute_script("arguments[0].click();", punch_button)
            logger.info("✅ Ponto batido com sucesso!")

    except Exception as e:
        msg = f"[ERRO] Falha durante a automação: {e}"
        logger.exception(msg)
        send_email("Erro ao bater ponto", msg)
    finally:
        driver.quit()
        logger.info("Driver encerrado.")
