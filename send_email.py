# --- SCRIPT PARA DEPLOY EN RENDER ---

# INSTALAR DEPENDENCIAS EN ENTORNOS LOCALES (comentado en Render)
# !pip install selenium requests urllib3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import time
import os

# --- FUNCION PRINCIPAL ---
def send_usdt_bob_email():
    # CONFIGURACIÓN DEL USUARIO
    EMAIL_USER = 'zambrano.jc.uy@gmail.com'                # <-- Cambia esto
    EMAIL_PASSWORD = 'vfoybmvnhxdwnlmm'               # <-- Cambia esto
    EMAIL_SEND = 'zambrano.jc@gmail.com'   # <-- Cambia esto
    EMAIL_CC = 'gonzalo.gutierrez@tecnofarma.com.bo'                                  # <-- Opcional
    SUBJECT = 'Tipo de Cambio USDT/BOB - Diario'
    URL = "https://p2p.army/en/p2p/fiats/BOB"

    # CONFIGURAR CHROME HEADLESS
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=2560x1600")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(15)
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(3)

    screenshot_path = "usdt_bob.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()

    # PREPARAR EMAIL
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_SEND
    msg['Cc'] = EMAIL_CC
    msg['Subject'] = SUBJECT

    body = "Adjunto gráfico de cotización USDT/BOB desde P2P Army."
    msg.attach(MIMEText(body, 'plain'))

    with open(screenshot_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename='usdt_bob.png')
        msg.attach(img)

    recipients = [EMAIL_SEND]
    if EMAIL_CC:
        recipients.append(EMAIL_CC)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, recipients, msg.as_string())
        server.quit()
        print("✅ Correo enviado exitosamente a:", recipients)
    except Exception as e:
        print("❌ Error al enviar correo:", str(e))

# --- EJECUTAR SOLO SI ES EL PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    send_usdt_bob_email()

# --- FIN DEL SCRIPT ---
