#Google Search - SEO bot 2025
#Kristian Gasic - kristian@gasic.bio

import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Liste von Schlüsselwörtern mit zugehörigen URLs
keywords_with_urls = {
    "empfohlen.net dsl vergleichen":
    "https://empfohlen.net/dsl-tarifvergleich/",
    "empfohlen.net kfz vergleichen":
    "https://empfohlen.net/kfz-versicherung/",
    "empfohlen.net Pionex trading bot":
    "https://empfohlen.net/pionex-1-crypto-trading-bot-2024/",
    "empfohlen.net n26 bank":
    "https://empfohlen.net/vertraut-n26-nicht/",
    "empfohlen.net c24 tagesgeld":
    "https://empfohlen.net/c24-bank-girokonto-und-tagesgeld/",
    "empfohlen.net tarifvergleiche dsl":
    "https://empfohlen.net/dsl-tarifvergleich/",
}

# Liste von Benutzeragenten für die Rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
]


# Funktion zur Auswahl eines zufälligen Schlüsselworts und der zugehörigen URL
def get_random_keyword_and_url():
    keyword = random.choice(list(keywords_with_urls.keys()))
    url = keywords_with_urls[keyword]
    return keyword, url


# Erstellen eines neuen temporären Browsers
def create_driver():
    options = Options()
    options.headless = True  # Führen Sie den Browser im Hintergrund aus
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_preference("intl.accept_languages",
                           "de-DE,de")  # Sprache auf Deutsch setzen

    # Wähle einen zufälligen Benutzeragenten aus
    user_agent = random.choice(user_agents)
    options.set_preference("general.useragent.override", user_agent)

    # Erstellen der Firefox-Instanz
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()),
                               options=options)

    # Zufällige Fenstergröße setzen
    window_size = random.choice([(1920, 1080), (1440, 900),
                                 (375, 667)])  # Einige Beispielgrößen
    driver.set_window_size(window_size[0], window_size[1])

    return driver


# Funktion zur Durchführung einer Google-Suche und zum Öffnen der entsprechenden URL
def perform_search():
    driver = create_driver()

    try:
        keyword, expected_url = get_random_keyword_and_url()

        print(f"Durchsuche Google nach: {keyword}")

        # Suchanfrage an Google
        driver.get("https://www.google.de")

        # Akzeptiere Cookies und Nutzungsbedingungen
        accept_cookies_and_terms(driver)

        # Suchfeld finden und Suche durchführen
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword)
        search_box.submit()

        # Warte bis die Ergebnisse geladen sind
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h3')))

        # Suche nach dem spezifischen Link in den Ergebnissen
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')
        target_url_found = False

        for result in results:
            try:
                # Hole den Link des Suchergebnisses
                parent_element = result.find_element(
                    By.XPATH, '..')  # Zum Elternelement (den Link) navigieren
                link = parent_element.get_attribute('href')

                # Überprüfen, ob der Link mit der erwarteten URL übereinstimmt
                if expected_url in link:  # Nutze 'in', um sicherzustellen, dass wir auch mit Weiterleitungen übereinstimmen
                    print(f"Öffne die Ziel-URL: {expected_url}")
                    # Scrolle zum Element und klicke darauf
                    driver.execute_script("arguments[0].scrollIntoView();",
                                          result)
                    result.click()  # Klicke auf das Ergebnis
                    target_url_found = True
                    break
            except Exception as e:
                print(f"Fehler beim Zugriff auf das Ergebnis: {e}")

        # Wenn der Link nicht gefunden wurde, öffne die zugehörige URL direkt
        if not target_url_found:
            print(
                f"Die Ziel-URL wurde in den Ergebnissen nicht gefunden. Öffne stattdessen die URL direkt: {expected_url}"
            )
            driver.get(expected_url)  # Öffne die URL direkt

        # Wartezeit nach dem Öffnen der Ziel-URL
        time.sleep(random.randint(30, 45))

        # Führe zufällige Interaktionen auf der geöffneten Webseite durch
        perform_random_interactions(driver)

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    finally:
        # Lösche Cookies und schließe die Browser-Session
        driver.delete_all_cookies()  # Cookies löschen
        driver.quit()


# Funktion zur Akzeptierung von Cookies und Nutzungsbedingungen
def accept_cookies_and_terms(driver):
    try:
        # Versuche, den Cookie-Akzeptieren-Button zu finden und darauf zu klicken
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@id, 'L2AGLb') or contains(text(), 'Alle akzeptieren')]"
            )))
        # Scrollen Sie zu dem Element, um sicherzustellen, dass es sichtbar ist
        driver.execute_script("arguments[0].scrollIntoView(true);",
                              cookie_accept_button)
        time.sleep(
            1
        )  # Warten Sie kurz, um sicherzustellen, dass das Element in Sicht ist
        cookie_accept_button.click()
        print("Cookies akzeptiert.")
    except Exception as e:
        print(f"Fehler beim Akzeptieren der Cookies: {e}")

    try:
        # Versuche, den Nutzungsbedingungen-Button zu finden und darauf zu klicken
        terms_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'Zustimmen')]")))
        # Scrollen Sie zu dem Element, um sicherzustellen, dass es sichtbar ist
        driver.execute_script("arguments[0].scrollIntoView(true);",
                              terms_accept_button)
        time.sleep(
            1
        )  # Warten Sie kurz, um sicherzustellen, dass das Element in Sicht ist
        terms_accept_button.click()
        print("Nutzungsbedingungen akzeptiert.")
    except Exception as e:
        print(f"Fehler beim Akzeptieren der Nutzungsbedingungen: {e}")


# Funktion für zufällige Interaktionen auf der Webseite
def perform_random_interactions(driver):
    # Führe zufällige Scroll- und Klickaktionen durch
    for _ in range(random.randint(3, 5)):  # Anzahl der Interaktionen
        time.sleep(random.uniform(
            2, 5))  # Zufällige Wartezeit zwischen Interaktionen
        action = random.choice(['scroll', 'click'])

        if action == 'scroll':
            # Zufälliges Scrollen
            scroll_height = random.randint(200, 600)  # Zufällige Scrollhöhe
            driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            print("Gescrollt.")

        elif action == 'click':
            # Versuchen, ein zufälliges Element auf der Seite zu klicken
            try:
                clickable_elements = driver.find_elements(
                    By.XPATH,
                    "//a[contains(@href, '')]")  # Alle Links auf der Seite
                if clickable_elements:
                    element_to_click = random.choice(clickable_elements)
                    driver.execute_script("arguments[0].scrollIntoView(true);",
                                          element_to_click)
                    time.sleep(
                        1
                    )  # Wartezeit, um sicherzustellen, dass das Element sichtbar ist
                    element_to_click.click()
                    print(f"Auf das Element {element_to_click.text} geklickt.")
            except Exception as e:
                print(f"Fehler beim Klicken auf ein zufälliges Element: {e}")


# Hauptaufruf
if __name__ == "__main__":
    while True:  # Endlosschleife, um den Vorgang ständig zu wiederholen
        for _ in range(3):  # Führen Sie 3 Sitzungen durch
            perform_search()
        print("Warte 30-65 Sekunden, bevor der Vorgang erneut beginnt...")
        time.sleep(random.randint(30, 65))  # Wartezeit zwischen den Sitzungen
