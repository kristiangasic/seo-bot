# Google Search - SEO Bot 2025

### Overview
This project is a script designed for **practice purposes only** to automate simple Google searches and simulate user interactions on target web pages. It utilizes **Selenium WebDriver** with **Python** and requires a **Firefox browser**. Be aware of the potential risks of automated queries—Google may penalize such activities. Use responsibly and only within the bounds of legal and ethical guidelines.

---

### Features
- Randomized keyword-based Google searches.
- Simulates user interactions (scrolling, clicking links) on target web pages.
- Randomized user agents and browser window sizes for enhanced variability.
- Automated cookie and terms acceptance.

---

### Installation

#### 1. Prerequisites
- **Operating System:** Windows 10/11.
- **Browser:** Latest version of [Firefox](https://www.mozilla.org/en-US/firefox/new/).
- **Python Version:** Python 3.x.

#### 2. Required Python Packages
Run the following commands to install dependencies:
```bash
pip install selenium
pip install webdriver-manager
```

#### 3. Additional Downloads
- [Python](https://www.python.org/downloads/)
- [Selenium Documentation](https://www.selenium.dev/documentation/en/)
- [Webdriver Manager Documentation](https://pypi.org/project/webdriver-manager/)

---

### Usage

#### Running the Script
1. Clone this repository to your local machine.
2. Run the script using Python:
   ```bash
   python main.py
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
