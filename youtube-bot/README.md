## Deutsch - README.md

# Automatisiertes Google-Suchen und YouTube-Videointeraktionen

Dieses Skript ermöglicht die Automatisierung von Google-Suchen, das Abrufen von YouTube-Videos und das Interagieren mit den Videos, indem es Cookies akzeptiert, das Video abspielt und das Video für eine zufällige Zeitdauer zwischen 30 und 85 Sekunden schaut. Während der Wiedergabe wird der Bildschirm zufällig gescrollt, um Interaktivität zu simulieren.

## Funktionen

- **Google-Suche automatisiert**: Das Skript führt eine Google-Suche basierend auf zufälligen Keywords aus.
- **Zufällige Auswahl von YouTube-Links**: Nachdem die Google-Suche abgeschlossen ist, wird ein zufälliger YouTube-Link aus den Suchergebnissen ausgewählt und geöffnet.
- **Cookies akzeptieren**: Das Skript akzeptiert automatisch die Cookies auf Google und YouTube.
- **Autoplay und zufällige Wiedergabedauer**: Nach dem Laden des YouTube-Videos wird es abgespielt, und das Skript wartet zufällig zwischen 30 und 85 Sekunden. Während der Wiedergabe wird der Bildschirm mindestens einmal und höchstens dreimal gescrollt.
  
## Voraussetzungen

- Python 3.x
- Selenium
- Firefox-Webbrowser
- GeckoDriver (wird automatisch installiert)
- WebDriver Manager
- Windows 10 / 11

## Installation

1. **Python installieren**: Falls noch nicht geschehen, installiere Python 3.x von der [offiziellen Website](https://www.python.org/downloads/).

2. **Abhängigkeiten installieren**: Installiere die benötigten Python-Bibliotheken:
   ```bash
   pip3 install selenium webdriver-manager
   ```

3. **Führe das Skript aus**: Nachdem alle Abhängigkeiten installiert sind, führe das Skript aus:
   ```bash
   python3 main.py
   ```

## Funktionsweise des Skripts

1. **Google-Suche**: Das Skript führt eine Google-Suche basierend auf einem zufälligen Schlüsselwort aus und öffnet die ersten Suchergebnisse, die zu YouTube führen.
2. **Cookies akzeptieren**: Es wird überprüft, ob ein Cookie-Popup auf Google und YouTube angezeigt wird, und es wird automatisch akzeptiert.
3. **Video abspielen**: Nachdem das YouTube-Video geöffnet wurde, wird der Play-Button geklickt, und das Video wird für eine zufällige Zeitdauer zwischen 30 und 85 Sekunden abgespielt.
4. **Scrollen während der Wiedergabe**: Während der Wiedergabe wird der Bildschirm mindestens einmal, maximal dreimal gescrollt.

## Wichtige Hinweise

- Das Skript läuft kontinuierlich und wiederholt den Prozess, bis es manuell gestoppt wird.
- Die Google-Suchen erfolgen mit einer zufälligen Auswahl von Benutzeragenten, um das Skript realistischer zu machen.
- Das Skript funktioniert auf YouTube-Videos, die öffentlich zugänglich sind.

---

## English - README.md

# Automated Google Search and YouTube Video Interactions

This script automates Google searches, retrieves YouTube videos, and interacts with them by accepting cookies, playing the video, and watching the video for a random time between 30 and 85 seconds. During playback, the screen is randomly scrolled to simulate user interaction.

## Features

- **Automated Google Search**: The script performs a Google search based on random keywords.
- **Random YouTube Link Selection**: After completing the Google search, it selects and opens a random YouTube link from the search results.
- **Cookie Acceptance**: The script automatically accepts cookies on both Google and YouTube.
- **Autoplay and Random Playback Duration**: After the YouTube video loads, it plays the video, and the script waits for a random duration between 30 and 85 seconds. During playback, the screen is scrolled at least once and at most three times.
  
## Requirements

- Python 3.x
- Selenium
- Firefox Web Browser
- GeckoDriver (automatically installed)
- WebDriver Manager
- Windows 10 / 11

## Installation

1. **Install Python**: If you haven’t already, install Python 3.x from the [official website](https://www.python.org/downloads/).

2. **Install Dependencies**: Install the required Python libraries:
   ```bash
   pip3 install selenium webdriver-manager
   ```

3. **Run the Script**: After installing the dependencies, run the script:
   ```bash
   python main.py
   ```

## How the Script Works

1. **Google Search**: The script performs a Google search based on a random keyword and opens the first search results that lead to YouTube.
2. **Cookie Acceptance**: It checks if a cookie popup is shown on Google and YouTube, and automatically accepts it.
3. **Play Video**: Once the YouTube video is opened, it clicks the Play button and plays the video for a random duration between 30 and 85 seconds.
4. **Scrolling During Playback**: During playback, the screen is scrolled at least once, and at most three times.

## Important Notes

- The script runs continuously and repeats the process until manually stopped.
- Google searches are performed with a random selection of user agents to make the script appear more realistic.
- The script works on YouTube videos that are publicly available.

---
