# Multi-Engine Search - SEO Bot 2025

### Overview
This project is a script designed for **practice purposes only** to automate simple Google searches and simulate user interactions on target web pages. It utilizes **Selenium WebDriver** with **Python** and requires a **Firefox browser**. Be aware of the potential risks of automated queries—Google may penalize such activities. Use responsibly and only within the bounds of legal and ethical guidelines.


---

### Features
- **Multi-Engine Support**: Perform searches on Bing, DuckDuckGo, and Yahoo.
- **Proxy Rotation**: Automatically rotates proxies to ensure anonymity.
- **User-Agent Spoofing**: Randomly selects user-agents to mimic real browser activity.
- **Headless Browsing**: Uses headless Firefox for efficient and invisible operations.
- **Cookie Handling**: Automatically accepts cookie policies to prevent interruptions.
- **Customizable Search Duration**: Define the duration for which the bot should visit and scroll through the search results.
- **GUI Support**: User-friendly GUI for easy configuration and control of the bot.

---

### Installation

#### 1. Prerequisites
- **Operating System:** Windows 10/11.
- **Browser:** Latest version of [Firefox/Geckodriver](https://github.com/mozilla/geckodriver/releases).
- **Python Version:** Python 3.x.

#### 2. Required Python Packages
Run the following commands to install dependencies:
```bash
pip install selenium-wire
pip install fake_useragent
pip install customtkinter
pip install urllib3
pip install requests
```

#### 3. Additional Downloads
- [Python](https://www.python.org/downloads/)
- [Selenium Documentation](https://www.selenium.dev/documentation/en/)
- [Webdriver Manager Documentation](https://pypi.org/project/webdriver-manager/)
- [Youtube Tutorial here](https://www.youtube.com/watch?v=NKj2z_T5wkw)

---

### Usage

#### Running the Script
1. Clone this repository to your local machine.
2. Run the script using Python:
   ```bash
   python3 main.py
   ```

#### Script Logic
1. The script selects a random keyword from the predefined `keywords_with_urls` dictionary.
2. It launches a headless Firefox browser instance with a random user agent and window size.
3. Simulates a Google search for the keyword and navigates to the associated URL.
4. Performs interactions (scrolling, clicking links) to mimic human behavior.
5. Repeats the process with randomized delays between sessions.

---

### Key Functionalities

#### 1. Randomized Behavior
- **Keywords & URLs:** A random keyword and associated URL are selected for each search.
- **User Agents:** A random user agent is applied to each session.
- **Browser Window Size:** Resized to emulate various device types.

#### 2. Search and Navigation
- Simulates Google searches and checks if the target URL appears in the results.
- If not found, directly navigates to the predefined URL.

#### 3. Cookie and Terms Acceptance
- Automatically clicks on cookie and terms acceptance buttons when presented.

#### 4. Random Interactions
- Scrolls the page randomly and clicks on links to simulate user behavior.

#### Example Configuration:
The `keywords_with_urls` dictionary stores the keyword-URL pairs:
```python
keywords_with_urls = {
    "example keyword": "https://example.com/page1",
    "another keyword": "https://example.com/page2"
}
```

---

### Warnings
- **Legal Risks:** Automated web interactions may violate terms of service. Ensure you have proper authorization.
- **Google Penalties:** Automated queries could result in IP bans or other restrictions.
- **Headless Browsing:** Although this script runs in headless mode, detection mechanisms may still recognize automation.

---

### Contributing
Feel free to submit issues or contribute enhancements via pull requests.

---

### Contact
For business inquiries, reach out to:  
**Kristian Gasic**  
📧 kristian@gasic.bio

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/kristiangasic)
