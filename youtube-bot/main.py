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
    "google search bot 2025 video": "https://www.youtube.com/watch?v=FwXxlSh61eI",
    "seo bot google 2025": "https://www.youtube.com/watch?v=FwXxlSh61eI",
    # Weitere Keywords und Links können hinzugefügt werden
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
    options.set_preference("intl.accept_languages", "de-DE,de")  # Sprache auf Deutsch setzen

    # Wähle einen zufälligen Benutzeragenten aus
    user_agent = random.choice(user_agents)
    options.set_preference("general.useragent.override", user_agent)

    # Erstellen der Firefox-Instanz
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    # Zufällige Fenstergröße setzen
    window_size = random.choice([(1920, 1080), (1440, 900), (375, 667)])  # Einige Beispielgrößen
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

        # Akzeptiere Cookies und Nutzungsbedingungen auf Google
        accept_cookies_and_terms(driver)

        # Suchfeld finden und Suche durchführen
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword)
        search_box.submit()

        # Warte bis die Ergebnisse geladen sind
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h3')))

        # Öffne direkt die Ziel-URL
        print(f"Öffne direkt die Ziel-URL: {expected_url}")
        driver.get(expected_url)

        # Cookies akzeptieren auf YouTube
        accept_youtube_cookies(driver)

        # Autoplay des Videos starten
        autoplay_video(driver)

        # Wartezeit nach dem Öffnen der Ziel-URL und der Video-Wiedergabe
        time.sleep(random.randint(30, 85))

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    finally:
        # Lösche Cookies und schließe die Browser-Session
        driver.delete_all_cookies()  # Cookies löschen
        driver.quit()

# Funktion zur Akzeptierung von Cookies und Nutzungsbedingungen auf Google
def accept_cookies_and_terms(driver):
    try:
        # Versuche, den neuen "Alle akzeptieren"-Button zu finden und darauf zu klicken
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                "//button[contains(@aria-label, 'Verwendung von Cookies und anderen Daten zu den beschriebenen Zwecken akzeptieren') or contains(., 'Alle akzeptieren')]"
            ))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", cookie_accept_button)
        time.sleep(1)  # Warten Sie kurz
        cookie_accept_button.click()
        print("Cookies akzeptiert auf Google.")
    except Exception as e:
        print(f"Fehler beim Akzeptieren der Cookies: {e}")

# Funktion zur Akzeptierung von YouTube-Cookies
def accept_youtube_cookies(driver):
    try:
        print("Überprüfe, ob das Cookie-Popup auf YouTube angezeigt wird...")

        # Warte, bis das Cookie-Popup sichtbar ist
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@aria-label, 'Verwendung von Cookies und anderen Daten zu den beschriebenen Zwecken akzeptieren') or contains(., 'Alle akzeptieren')]"
            ))
        )

        # Scrolle zum Button (falls nötig) und klicke darauf
        driver.execute_script("arguments[0].scrollIntoView(true);", cookie_accept_button)
        time.sleep(1)  # Warte kurz
        cookie_accept_button.click()
        print("Cookies auf YouTube akzeptiert.")
    except Exception as e:
        print(f"Fehler beim Akzeptieren der Cookies auf YouTube: {e}")

# Funktion zum Starten des Videos und Autoplay simulieren
def autoplay_video(driver):
    try:
        # Warte darauf, dass der Play-Button sichtbar wird
        play_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-play-button"))
        )
        play_button.click()  # Klick auf den Play-Button
        print("Video abgespielt.")
        
        # Scrollen während der Wiedergabezeit (zwischen 1 bis 3 mal)
        scroll_count = random.randint(1, 3)  # Wählen Sie eine zufällige Anzahl an Scrolls
        for _ in range(scroll_count):
            time.sleep(random.randint(5, 15))  # Warte eine zufällige Zeitspanne
            driver.execute_script("window.scrollBy(0, 300);")  # Scrollt nach unten
            print("Gesrollt während der Wiedergabe.")
    except Exception as e:
        print(f"Fehler beim Abspielen des Videos: {e}")

# Hauptaufruf
if __name__ == "__main__":
    while True:  # Endlosschleife, um den Vorgang ständig zu wiederholen
        for _ in range(3):  # Führen Sie 3 Sitzungen durch
            perform_search()
        print("Warte 30-65 Sekunden, bevor der Vorgang erneut beginnt...")
        time.sleep(random.randint(30, 65))  # Wartezeit zwischen den Sitzungen
