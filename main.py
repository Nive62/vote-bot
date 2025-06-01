import re
import random
import time
import sys
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# Constantes
PSEUDO_VOTE = "Bapt62"
URL_VOTE = "https://www.moncube.eu/vote/"

# Logger
def log(message):
    now = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    print(f"[{now}] : {message}")

# Capture écran en cas de debug
def take_screenshot(step_name):
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    filename = f"screenshot_{step_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    log(f"Capture d'écran prise : {filename}")

# Attente du compte à rebours
def wait():
    time.sleep(3)
    try:
        countdown_element = driver.find_element(By.ID, "countdown")
        countdown_text = countdown_element.text

        if not countdown_text or countdown_text == "Tu peux de nouveau voter":
            log("Bug ou retour immédiat possible, tentative de vote...")
            vote()
            return

        log(f"Temps restant avant de pouvoir revoter : {countdown_text}")
        match = re.match(r"(\d+)h (\d+)m (\d+)s", countdown_text)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            total_seconds = hours * 3600 + minutes * 60 + seconds

            log(f"Attente de {total_seconds} secondes...")
            time.sleep(total_seconds)
            vote()
        else:
            log("Format du compte à rebours inconnu, tentative immédiate...")
            vote()
    except NoSuchElementException:
        log("Élément countdown introuvable, tentative de vote immédiate...")
        vote()
    except KeyboardInterrupt:
        log("Interruption manuelle du script.")
        sys.exit()
    except Exception as e:
        log(f"Erreur inattendue dans wait(): {str(e)}")
        vote()

# Fonction de vote
def vote():
    try:
        log("Tentative de vote en cours...")
        pseudo_input = driver.find_element(By.ID, 'pseudo')
        pseudo_input.send_keys(PSEUDO_VOTE)

        time.sleep(random.uniform(0.5, 2.5))

        submit_button = driver.find_element(By.ID, "submit-button")
        submit_button.click()

        time.sleep(2)

        try:
            countdown_element = driver.find_element(By.ID, "countdown")
            log("Vote déjà effectué, passage en attente.")
            wait()
        except NoSuchElementException:
            log("Vote validé. Attente du visionnage...")
            time.sleep(45)
            driver.refresh()
            time.sleep(5)
            wait()
    except NoSuchElementException:
        log("Champs de vote absents, on attend...")
        wait()
    except KeyboardInterrupt:
        log("Interruption manuelle du script.")
        sys.exit()
    except Exception as e:
        log(f"Erreur inattendue dans vote(): {str(e)}")
        wait()

# Lancement
if __name__ == "__main__":
    log("Démarrage du script...")

    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--mute-audio")

        driver = uc.Chrome(options=options, version_main=136)
        driver.get(URL_VOTE)
        vote()
    except Exception as e:
        log(f"Erreur critique au démarrage : {str(e)}")
        take_screenshot("crash_startup")
        sys.exit()
