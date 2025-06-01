# -*- coding: utf-8 -*-
import os
import subprocess

def installer_chrome():
    print("Installation de Chromium stable...")
    subprocess.run(["apt-get", "update"], check=True)
    subprocess.run(["apt-get", "install", "-y", "wget", "unzip", "curl", "gnupg", "ca-certificates", "fonts-liberation", "libappindicator3-1", "libasound2", "libatk-bridge2.0-0", "libatk1.0-0", "libcups2", "libdbus-1-3", "libgdk-pixbuf2.0-0", "libnspr4", "libnss3", "libx11-xcb1", "libxcomposite1", "libxdamage1", "libxrandr2", "xdg-utils", "libu2f-udev", "libvulkan1"], check=True)
    subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], check=True)
    subprocess.run(["dpkg", "-i", "google-chrome-stable_current_amd64.deb"], check=False)
    subprocess.run(["apt-get", "-f", "install", "-y"], check=True)
    print("✅ Chromium installé avec succès.")

installer_chrome()

import re
import random
import time
import sys
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# Debug
def take_screenshot(step_name):
    now = datetime.now()
    date = now.strftime("%d%m%Y_%H%M%S")
    filename = f"screenshot_{step_name}_{date}.png"
    driver.save_screenshot(filename)
    log(f"Capture d'écran prise : {filename}")

pseudo_vote = "Bapt62"
ip = "https://www.moncube.eu/vote/"

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

            log(f"Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}")

            # Convertir le temps total en secondes
            total_seconds = hours * 3600 + minutes * 60 + seconds
            log(f"Temps total en secondes: {total_seconds}")

            # Attendre pendant le temps total en secondes
            try:
                time.sleep(total_seconds)
                vote()
            except KeyboardInterrupt:
                log("Interruption programme 1 ")
                sys.exit()
            except Exception as e:
                log("Erreur "+str(e)+" tentative de vote à nouveau...")
                vote()
    except NoSuchElementException as e:
        log("Erreur NoSuchElementException wait(), retentative de vote...")
        vote()
    except KeyboardInterrupt:
        log("Interruption programme 3")
        sys.exit()
    except Exception as e:
        log("Erreur inconnue wait() : "+str(e))
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
        except NoSuchElementException as e:
            time.sleep(45)
            log("Fin du visionnage")

            driver.get(driver.current_url)
            time.sleep(3)
            driver.refresh()
            time.sleep(5)
            
            wait()
    except NoSuchElementException as e:
        log("Erreur NoSuchElementException vote() (vote déjà effectué)")
        wait()
    except KeyboardInterrupt:
        log("Interruption programme 3")
        sys.exit()
    except Exception as e:
        log("Erreur "+str(e)+" vote() (vote déjà effectué ou autre)")
        wait()

if __name__ == "__main__":
    log("Démarrage")

    options = uc.ChromeOptions()  
    
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--mute-audio")

    driver = uc.Chrome(options=options,)



    driver.get(ip)
    vote()
