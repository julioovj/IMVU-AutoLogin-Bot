import yaml
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

def yaml_loader(filepath):
    with open(filepath, "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def site_login(driver, url, username, password):
    driver.get(url)
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sign-in'))).click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'avatarname'))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password'))).send_keys(password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))).click()
        time.sleep(5)
    except (TimeoutException, NoSuchElementException):
        site_login(driver, url, username, password)

config = yaml_loader("config.yml")
options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
options.add_argument('--incognito')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-logging')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--silent')
options.add_argument('--disable-infobars')
options.add_argument('--disable-web-security')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--headless')

# Redirecionar logs do serviço para null
service = Service(log_path=os.devnull)

driver = webdriver.Chrome(service=service, options=options)
site_login(driver, "https://secure.imvu.com/welcome/login/", config["account"]["username"], config["account"]["password"])

print("Login concluído. Pressione Ctrl+C no console para encerrar.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Encerrando o navegador.")
    driver.quit()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    driver.quit()
