import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def installer_chrome():
    subprocess.run(["apt-get", "update"], check=True)
    subprocess.run(["apt-get", "install", "-y", "wget", "unzip", "curl", "gnupg", "ca-certificates",
                    "fonts-liberation", "libappindicator3-1", "libasound2t64", "libatk-bridge2.0-0",
                    "libatk1.0-0", "libcups2", "libdbus-1-3", "libgdk-pixbuf2.0-0", "libnspr4",
                    "libnss3", "libx11-xcb1", "libxcomposite1", "libxdamage1", "libxrandr2",
                    "xdg-utils", "libu2f-udev", "libvulkan1"], check=True)
    print("Chromium installé")

def lancer_vote():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get("https://example.com")  # Remplace par ton URL
    print("Ouverture du site...")

    try:
        bouton_vote = driver.find_element(By.ID, "vote-button")  # Remplace par l'ID correct
        bouton_vote.click()
        print("Vote effectué.")
    except Exception as e:
        print("Erreur lors du vote :", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    installer_chrome()
    while True:
        lancer_vote()
        print("Attente avant le prochain vote...")
        time.sleep(3600)  # Une heure d'attente
