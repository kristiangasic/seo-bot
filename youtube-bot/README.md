# Youtube Views Bot with and without Proxys.

This script uses **Selenium** and **Proxies** to simulate human-like behavior on YouTube by performing automatic Google searches, opening YouTube videos, and interacting with them. It includes support for rotating proxies from a `.txt` file, which should be provided in a specific format.

## How it Works

1. **Google Search**: The script searches for predefined keywords on Google.
2. **Open YouTube Link**: After the search, the script opens the associated YouTube link, which is linked with the keyword, and starts playing the video.
3. **Proxy Rotation**: Each new session uses a random proxy from a `.txt` file, simulating a different IP address. This file must be in the same directory as the script and follows this format:  
   `IP:PORT:USER:PASSWORD`

**Example of `proxies.txt` content:**
```
173.0.9.209:5792:hgtpuldo:YourPassword
92.22.34.56:1080:user1:pass1
...
```

### Changes

#### Proxy Support

- The script loads proxies from the `proxies.txt` file and selects a random proxy for each new session.
- Each proxy follows the format `IP:PORT:USER:PASSWORD` and is used to change the IP address for each session.

### Updates in the Script

- Proxies are automatically loaded from the `proxies.txt` file.
- A random proxy is selected for each new `webdriver` instance, providing extra anonymity.
- **Selenium WebDriver** is configured to use proxies for every new session.

## Requirements

- Python 3.x
- Selenium
- Geckodriver (for Firefox)
- WebDriver Manager
- Proxies in a `proxies.txt` file
- Windows 10 / 11

### Installation

1. **Install dependencies:**
   ```bash
   pip3 install selenium
   pip3 install webdriver-manager
   ```

2. **Proxies**: You can get free proxies from Webshare. Sign up and use the referral link to get **10 free proxies**:
   [Webshare Proxies (10 free proxies)](https://www.webshare.io/?referral_code=b3hfjb3ndfih)

3. **Create the `proxies.txt`** file in the same directory as the script and add your proxies in the following format:
   ```
   173.0.9.209:5792:hgtpuldo:YourPassword
   92.22.34.56:1080:user1:pass1
   ...
   ```

### Running the Script

1. Download the script and ensure the `proxies.txt` is in the same folder as the script.
2. Run the script:
   ```bash
   python3 main.py
   ```

3. The script will now **search Google**, **open a random YouTube video**, and **rotate proxies** for each new session.

### Note on Webshare Proxies

You can get **10 free proxies** from Webshare by signing up using the referral link and using the **Referral Code**:
[Webshare Proxies (10 free proxies)](https://www.webshare.io/?referral_code=b3hfjb3ndfih)

## Important Notes

- **Proxies**: Make sure your `proxies.txt` is correctly formatted and contains valid proxies.
- **Human-like Behavior**: The script includes functions to simulate human-like behavior, such as slow typing and random time delays.
- **Webshare**: You can use Webshare proxies or any other proxy service you prefer. Webshare provides an easy way to access 10 free proxies.

---
