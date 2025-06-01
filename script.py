# -*- coding: utf-8 -*-
import os
import subprocess
import re
import random
import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service


# ───── Installation Chromium (Railway) ─────
def installer_chromium():
    print("Installation de Chromium et Chromedriver...")
    subprocess.run(["apt-get", "update"], check=True)
    subprocess.run(["apt-get", "install", "-y", "chromium", "chromium-driver"], check=True)
    print("Chromium installé")

installer_chromium()

# ───── Variables Globales ─────
pseudo_vote = "Bapt62"
ip = "https://www.moncube.eu/vote/"

# ───── Fonctions Utiles ─────
def log(text):
    now = datetime.now()
    date = now.strftime("%d/%m/%Y à %H:%M:%S")
    print("["+date+"] : "+text)

def wait():
    time.sleep(3)
    try:
        countdown_element = driver.find_element(By.ID, "countdown")
        countdown_text = countdown_element.text
        if not countdown_text and countdown_element != "Tu peux de nouveau voter":
            log("Bug de countdown, on attend encore...")
            wait()
        log(f"Temps restant avant de pouvoir revoter: {countdown_text}")
        match = re.match(r"(\d+)h (\d+)m (\d+)s", countdown_text)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))

            total_seconds = hours * 3600 + minutes * 60 + seconds
            log(f"Temps total en secondes: {total_seconds}")

            try:
                time.sleep(total_seconds)
                vote()
            except KeyboardInterrupt:
                log("Interruption programme 1")
                sys.exit()
            except Exception as e:
                log("Erreur "+str(e)+", tentative de vote à nouveau...")
                vote()
    except NoSuchElementException:
        log("Erreur NoSuchElementException wait(), tentative de vote...")
        vote()
    except KeyboardInterrupt:
        log("Interruption programme 3")
        sys.exit()
    except Exception as e:
        log("Erreur inconnue wait(): "+str(e))
        vote()

def vote():
    try:
        log("Vote en cours")
        pseudo = driver.find_element(By.ID, 'pseudo')
        pseudo.send_keys(pseudo_vote)

        time.sleep(random.randint(500, 2500) / 1000)

        valider = driver.find_element(By.ID, "submit-button")
        valider.click()

        try:
            countdown_element = driver.find_element(By.ID, "countdown")
            log("Vote déjà effectué")
            wait()
        except NoSuchElementException:
            time.sleep(45)
            log("Fin du visionnage")

            driver.get(driver.current_url)
            time.sleep(3)
            driver.refresh()
            time.sleep(5)

            wait()
    except NoSuchElementException:
        log("Erreur NoSuchElementException vote() (vote déjà effectué)")
        wait()
    except KeyboardInterrupt:
        log("Interruption programme 3")
        sys.exit()
    except Exception as e:
        log("Erreur "+str(e)+" vote()")
        wait()

# ───── Démarrage Selenium ─────
log("Démarrage")

options = webdriver.ChromeOptions()
options.binary_location = "/snap/bin/chromium"
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/snap/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)


driver.get(ip)
vote()
