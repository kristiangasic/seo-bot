import json
import os
import time
import random
import requests
from datetime import datetime
from threading import Thread, Event
from queue import Queue
from seleniumwire import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import customtkinter as ctk
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SearchBot:
    def __init__(self, root):
        self.root = root
        self.stop_event = Event()
        self.proxy_queue = Queue()
        self.keywords_with_urls = {}
        self.user_agents_list = []
        self.concurrent_browsers = 3
        self.visit_duration = (60, 300)  # min, max seconds
        self.working_proxies_file = "working_proxies.json"
        self.keywords_file = "keywords.txt"
        self.user_agents_file = "user_agents.txt"
        self.geonode_api_url = "https://proxylist.geonode.com/api/proxy-list?protocols=http%2Chttps&limit=500&page=1&sort_by=lastChecked&sort_type=desc"
        self.working_proxies = self.load_working_proxies()
        self.threads = []

        # Default keywords and user agents
        self.default_keywords = {
            "product reviews": "https://empfohlen.net/product-review/",
            "earn 500 euros tax-free Christmas bonus": "https://empfohlen.net/500-euro-steuerfreies-weihnachtsgeld-verdienen-so-einfach-gehts/",
            "latest news updates": "https://empfohlen.net/news/"
        }
        
        self.default_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
        ]

        # Load saved keywords and user agents
        self.load_keywords()
        self.load_user_agents()

        # Search engines configuration
        self.search_engines = {
            'bing': {
                'url': 'https://www.bing.com',
                'search_box': 'q',
                'cookie_selectors': [
                    "button[contains(., 'Accept')]",
                    "button[contains(., 'Akzeptieren')]",
                    "#bnp_btn_accept"
                ]
            },
            'duckduckgo': {
                'url': 'https://duckduckgo.com',
                'search_box': 'q',
                'cookie_selectors': []  # DuckDuckGo doesn't use cookie consent
            },
            'yahoo': {
                'url': 'https://search.yahoo.com',
                'search_box': 'p',
                'cookie_selectors': [
                    "//button[@class='btn secondary accept-all ' and @name='agree']"
                ]
            }
        }

    def load_working_proxies(self):
        try:
            if os.path.exists(self.working_proxies_file):
                with open(self.working_proxies_file, 'r') as f:
                    data = json.load(f)
                    current_time = datetime.now()
                    working_proxies = {}
                    for proxy, timestamp in data.items():
                        last_check = datetime.fromisoformat(timestamp)
                        if (current_time - last_check).total_seconds() < 86400:  # 24 hours
                            working_proxies[proxy] = timestamp
                    return working_proxies
            return {}
        except json.JSONDecodeError:
            print(f"Error loading working proxies: Invalid JSON format in {self.working_proxies_file}")
            return {}
        except Exception as e:
            print(f"Error loading working proxies: {e}")
            return {}

    def save_working_proxies(self):
        try:
            with open(self.working_proxies_file, 'w') as f:
                json.dump(self.working_proxies, f)
        except Exception as e:
            print(f"Error saving working proxies: {e}")

    def save_working_proxy(self, proxy):
        try:
            self.working_proxies[proxy] = datetime.now().isoformat()
            self.save_working_proxies()
        except Exception as e:
            print(f"Error saving working proxy: {e}")

    def load_keywords(self):
        try:
            if os.path.exists(self.keywords_file):
                with open(self.keywords_file, 'r') as f:
                    for line in f:
                        keyword, url = line.strip().split('|')
                        self.keywords_with_urls[keyword] = url
            if not self.keywords_with_urls:
                self.keywords_with_urls = self.default_keywords.copy()
        except Exception as e:
            print(f"Error loading keywords: {e}")

    def save_keywords(self):
        try:
            with open(self.keywords_file, 'w') as f:
                for keyword, url in self.keywords_with_urls.items():
                    f.write(f"{keyword}|{url}\n")
        except Exception as e:
            print(f"Error saving keywords: {e}")

    def load_user_agents(self):
        try:
            if os.path.exists(self.user_agents_file):
                with open(self.user_agents_file, 'r') as f:
                    self.user_agents_list = [line.strip() for line in f]
            if not self.user_agents_list:
                self.user_agents_list = self.default_user_agents.copy()
        except Exception as e:
            print(f"Error loading user agents: {e}")

    def save_user_agents(self):
        try:
            with open(self.user_agents_file, 'w') as f:
                for user_agent in self.user_agents_list:
                    f.write(f"{user_agent}\n")
        except Exception as e:
            print(f"Error saving user agents: {e}")

    def fetch_geonode_proxies(self):
        try:
            response = requests.get(self.geonode_api_url, verify=False, timeout=10)
            if response.status_code == 200:
                data = response.json()
                proxies = []
                for item in data.get('data', []):
                    proxy = f"{item['ip']}:{item['port']}"
                    proxies.append(proxy)
                print(f"Fetched {len(proxies)} proxies from Geonode")
                return proxies
        except Exception as e:
            print(f"Error fetching Geonode proxies: {e}")
        return []

    def check_proxy(self, proxy):
        try:
            proxy_parts = proxy.split(":")
            if len(proxy_parts) == 4:
                # Authenticated proxy
                proxy_auth = f"{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}"
                proxy_dict = {
                    "http": f"http://{proxy_auth}",
                    "https": f"http://{proxy_auth}"
                }
            else:
                # Regular proxy
                proxy_dict = {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}"
                }
            response = requests.get(
                "https://ipv4.webshare.io/",
                proxies=proxy_dict,
                timeout=10,  # Erhöhtes Timeout
                verify=False
            )
            if response.status_code == 200:
                self.save_working_proxy(proxy)
                return True
        except Exception as e:
            print(f"Error checking proxy {proxy}: {e}")
        return False

    def get_random_proxy(self):
        if not self.proxy_queue.empty():
            proxy = self.proxy_queue.get()
            
            if proxy in self.working_proxies:
                self.proxy_queue.put(proxy)
                return proxy
                
            if self.check_proxy(proxy):
                self.proxy_queue.put(proxy)
                return proxy
            else:
                print(f"Proxy {proxy} failed, trying another")
                return self.get_random_proxy()
        return None

    def load_proxies(self, proxy_file="proxy-pro.txt", proxy_type="premium"):
        # Clear the proxy queue
        while not self.proxy_queue.empty():
            self.proxy_queue.get()
        
        if proxy_type == "free":
            # Load cached working proxies
            fresh_proxies = self.fetch_geonode_proxies()
            current_proxies = set(self.working_proxies.keys())
            new_proxies = set(fresh_proxies) - current_proxies
            
            # If the cache is empty or there are new proxies, update the cache
            if not current_proxies or new_proxies:
                for proxy in fresh_proxies:
                    self.working_proxies[proxy] = datetime.now().isoformat()
                self.save_working_proxies()
            
            for proxy in self.working_proxies.keys():
                self.proxy_queue.put(proxy)
                print(f"Loaded cached working proxy: {proxy}")

        elif proxy_type == "premium" and os.path.exists(proxy_file):
            # Load premium proxies from file
            try:
                with open(proxy_file, "r") as file:
                    for line in file:
                        proxy = line.strip()
                        if proxy:
                            self.proxy_queue.put(proxy)
                            print(f"Loaded premium proxy: {proxy}")
            except Exception as e:
                print(f"Error loading proxies from file: {e}")

        print(f"Loaded {self.proxy_queue.qsize()} total proxies")

    def create_driver(self, proxy=None):
        try:
            options = Options()
            options.headless = True
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-infobars")
            options.add_argument("--start-maximized")
            options.set_preference("intl.accept_languages", "de-DE,de")
            
            user_agent = random.choice(self.user_agents_list)
            options.set_preference("general.useragent.override", user_agent)

            seleniumwire_options = {}
            if proxy:
                proxy_parts = proxy.split(":")
                if len(proxy_parts) == 4:
                    # Authenticated proxy
                    proxy_ip, proxy_port, proxy_user, proxy_pass = proxy_parts
                    proxy_auth = f"{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}"
                    seleniumwire_options = {
                        'proxy': {
                            'http': f'http://{proxy_auth}',
                            'https': f'https://{proxy_auth}',
                            'no_proxy': 'localhost,127.0.0.1'
                        }
                    }
                    print(f"Using authenticated proxy: {proxy_ip}:{proxy_port}")
                else:
                    # Regular proxy
                    proxy_ip, proxy_port = proxy_parts
                    seleniumwire_options = {
                        'proxy': {
                            'http': f'http://{proxy_ip}:{proxy_port}',
                            'https': f'https://{proxy_ip}:{proxy_port}',
                            'no_proxy': 'localhost,127.0.0.1'
                        }
                    }
                    print(f"Using proxy: {proxy_ip}:{proxy_port}")

            geckodriver_path = os.path.join(os.getcwd(), 'geckodriver.exe')  # Lokaler Pfad zum geckodriver
            service = Service(executable_path=geckodriver_path)

            driver = webdriver.Firefox(service=service, options=options, seleniumwire_options=seleniumwire_options)

            window_size = random.choice([(1920, 1080), (1440, 900), (375, 667)])
            driver.set_window_size(window_size[0], window_size[1])
            return driver
        
        except Exception as e:
            print(f"Error creating driver: {e}")
            return None

    def accept_cookies(self, driver, search_engine):
        try:
            selectors = self.search_engines[search_engine]['cookie_selectors']
            for selector in selectors:
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    button.click()
                    print(f"Cookies accepted for {search_engine} using selector {selector}")
                    return True
                except Exception as e:
                    print(f"Failed to click on cookie button for {search_engine} using selector {selector}: {e}")
                    continue
        except Exception as e:
            print(f"Error while accepting cookies for {search_engine}: {e}")
        return False

    def perform_search(self, proxy=None):
        retry_attempts = 3  # Number of retry attempts
        while not self.stop_event.is_set():
            driver = None
            try:
                if not proxy:
                    proxy = self.get_random_proxy()
                
                driver = self.create_driver(proxy)
                if not driver:
                    proxy = self.get_random_proxy()
                    continue

                for keyword, url in self.keywords_with_urls.items():
                    if self.stop_event.is_set():
                        break

                    # Randomly select a search engine
                    search_engine = random.choice(list(self.search_engines.keys()))
                    search_config = self.search_engines[search_engine]

                    for attempt in range(retry_attempts):
                        try:
                            print(f"Searching for: {keyword} using {search_engine}, attempt {attempt + 1}")
                            driver.get(search_config['url'])
                            time.sleep(random.uniform(2, 4))
                            
                            # Accept cookies if necessary
                            self.accept_cookies(driver, search_engine)

                            break  # Exit retry loop on successful load
                        except Exception as e:
                            print(f"Failed to load {search_engine}, attempt {attempt + 1}: {e}")
                            if attempt == retry_attempts - 1:
                                # If final attempt fails, move to next proxy
                                proxy = self.get_random_proxy()
                                if driver:
                                    driver.quit()
                                driver = self.create_driver(proxy)
                                if not driver:
                                    continue
                            else:
                                time.sleep(random.uniform(2, 5))  # Wait before retrying

                    try:
                        search_box = WebDriverWait(driver, 20).until(  # Increased timeout
                            EC.presence_of_element_located((By.NAME, search_config['search_box']))
                        )
                        search_box.clear()
                        time.sleep(random.uniform(0.5, 1.5))
                        for char in keyword:
                            search_box.send_keys(char)
                            time.sleep(random.uniform(0.1, 0.3))
                        time.sleep(random.uniform(0.5, 1.5))
                        search_box.submit()

                        time.sleep(random.uniform(2, 4))

                        results = driver.find_elements(By.TAG_NAME, 'a')
                        found = False
                        
                        for result in results:
                            if self.stop_event.is_set():
                                break
                            
                            try:
                                href = result.get_attribute('href')
                                if href and url in href:
                                    driver.execute_script("arguments[0].scrollIntoView();", result)
                                    time.sleep(random.uniform(1, 2))
                                    result.click()
                                    found = True
                                    break
                            except Exception as e:
                                print(f"Error processing search result: {e}")
                                continue

                        if not found:
                            print(f"Target URL not found, navigating directly to: {url}")
                            driver.get(url)

                        # Random scrolling behavior
                        scroll_time = random.randint(self.visit_duration[0], self.visit_duration[1])
                        start_time = time.time()
                        while time.time() - start_time < scroll_time and not self.stop_event.is_set():
                            scroll_amount = random.randint(100, 800)
                            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                            time.sleep(random.uniform(2, 5))
                            
                            # Occasionally scroll back up
                            if random.random() < 0.3:
                                driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
                                time.sleep(random.uniform(1, 3))
                            
                    except Exception as e:
                        print(f"Error during search: {e}")
                        continue

                # After completing all keywords, wait before starting next cycle
                if not self.stop_event.is_set():
                    pause_time = random.randint(60, 120)
                    print(f"Completed keyword cycle. Pausing for {pause_time} seconds...")
                    time.sleep(pause_time)

            except Exception as e:
                print(f"Error in search thread: {e}")
            finally:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass

    def start_search(self, proxy_file, thread_count, keywords=None, user_agents=None, proxy_type="free", visit_duration=(60,300), concurrent_browsers=3):
        self.stop_event.clear()
        self.keywords_with_urls.clear()
        self.visit_duration = visit_duration
        self.concurrent_browsers = concurrent_browsers
        
        if keywords:
            for item in keywords.split(','):
                if '|' in item:
                    keyword, url = item.split('|')
                    self.keywords_with_urls[keyword.strip()] = url.strip()
        
        if not self.keywords_with_urls:
            self.keywords_with_urls = self.default_keywords.copy()

        self.user_agents_list = [ua.strip() for ua in user_agents.split(',')] if user_agents else self.default_user_agents.copy()

        # Save the keywords and user agents to files
        self.save_keywords()
        self.save_user_agents()

        self.load_proxies(proxy_file, proxy_type)
        
        self.threads = []
        for _ in range(min(thread_count, self.concurrent_browsers)):
            proxy = self.get_random_proxy()
            thread = Thread(target=self.perform_search, args=(proxy,))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()

    def stop_search(self):
        self.stop_event.set()
        for thread in self.threads:
            thread.join(timeout=5)
        self.root.quit()  # Quit the GUI


def create_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Multi-Engine Search Automation v1.0.2 github.com/kristiangasic")
    root.geometry("800x900")

    search_bot = SearchBot(root)

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    proxy_frame = ctk.CTkFrame(main_frame)
    proxy_frame.pack(fill="x", padx=10, pady=5)
    
    proxy_type_var = ctk.StringVar(value="free")
    ctk.CTkLabel(proxy_frame, text="Proxy Type:").pack(side="left", padx=5)
    ctk.CTkRadioButton(proxy_frame, text="Free Proxy", variable=proxy_type_var, value="free").pack(side="left", padx=5)
    ctk.CTkRadioButton(proxy_frame, text="Premium Proxy", variable=proxy_type_var, value="premium").pack(side="left", padx=5)

  
    settings_frame = ctk.CTkFrame(main_frame)
    settings_frame.pack(fill="x", padx=10, pady=5)
    
    thread_count_var = ctk.IntVar(value=3)
    concurrent_browsers_var = ctk.IntVar(value=3)
    
    thread_label_frame = ctk.CTkFrame(settings_frame)
    thread_label_frame.pack(fill="x", pady=2)
    ctk.CTkLabel(thread_label_frame, text="Thread Count:").pack(side="left", padx=5)
    thread_label = ctk.CTkLabel(thread_label_frame, textvariable=thread_count_var)
    thread_label.pack(side="right", padx=5)
    
    thread_slider = ctk.CTkSlider(settings_frame, from_=1, to=10, number_of_steps=9, variable=thread_count_var)
    thread_slider.pack(fill="x", padx=5, pady=2)
    
    browser_label_frame = ctk.CTkFrame(settings_frame)
    browser_label_frame.pack(fill="x", pady=2)
    ctk.CTkLabel(browser_label_frame, text="Concurrent Browsers:").pack(side="left", padx=5)
    browser_label = ctk.CTkLabel(browser_label_frame, textvariable=concurrent_browsers_var)
    browser_label.pack(side="right", padx=5)
    
    browser_slider = ctk.CTkSlider(settings_frame, from_=1, to=5, number_of_steps=4, variable=concurrent_browsers_var)
    browser_slider.pack(fill="x", padx=5, pady=2)

    duration_frame = ctk.CTkFrame(settings_frame)
    duration_frame.pack(fill="x", pady=5)
    
    visit_min_var = ctk.IntVar(value=60)
    visit_max_var = ctk.IntVar(value=300)
    
    duration_label_frame = ctk.CTkFrame(duration_frame)
    duration_label_frame.pack(fill="x")
    ctk.CTkLabel(duration_label_frame, text="Visit Duration (seconds):").pack(side="left", padx=5)
    ctk.CTkLabel(duration_label_frame, text="Min:").pack(side="left", padx=5)
    ctk.CTkLabel(duration_label_frame, textvariable=visit_min_var).pack(side="left", padx=2)
    ctk.CTkLabel(duration_label_frame, text="Max:").pack(side="left", padx=5)
    ctk.CTkLabel(duration_label_frame, textvariable=visit_max_var).pack(side="left", padx=2)
    
    min_slider = ctk.CTkSlider(duration_frame, from_=30, to=180, number_of_steps=150, variable=visit_min_var)
    min_slider.pack(fill="x", padx=5, pady=2)
    
    max_slider = ctk.CTkSlider(duration_frame, from_=181, to=600, number_of_steps=419, variable=visit_max_var)
    max_slider.pack(fill="x", padx=5, pady=2)

    keywords_frame = ctk.CTkFrame(main_frame)
    keywords_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    ctk.CTkLabel(keywords_frame, text="Keywords (keyword|url):").pack(anchor="w", padx=5, pady=2)
    keywords_text = ctk.CTkTextbox(keywords_frame, height=150)
    keywords_text.pack(fill="both", expand=True, padx=5, pady=2)
    default_keywords = "\n".join([f"{k}|{v}" for k, v in search_bot.keywords_with_urls.items()])
    keywords_text.insert("1.0", default_keywords)

    agents_frame = ctk.CTkFrame(main_frame)
    agents_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    ctk.CTkLabel(agents_frame, text="User Agents:").pack(anchor="w", padx=5, pady=2)
    agents_text = ctk.CTkTextbox(agents_frame, height=150)
    agents_text.pack(fill="both", expand=True)
    agents_text.insert("1.0", "\n".join(search_bot.user_agents_list))

    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(fill="x", padx=10, pady=5)
    
    start_button = ctk.CTkButton(
        button_frame,
        text="Start",
        command=lambda: search_bot.start_search(
            "proxy.txt" if proxy_type_var.get() == "free" else "proxy-pro.txt",
            thread_count_var.get(),
            keywords_text.get("1.0", "end-1c").replace("\n", ","),
            agents_text.get("1.0", "end-1c").replace("\n", ","),
            proxy_type_var.get(),
            (visit_min_var.get(), visit_max_var.get()),
            concurrent_browsers_var.get()
        )
    )
    start_button.pack(side="left", padx=5)

    stop_button = ctk.CTkButton(
        button_frame,
        text="Stop",
        command=search_bot.stop_search
    )
    stop_button.pack(side="left", padx=5)

    root.protocol("WM_DELETE_WINDOW", search_bot.stop_search)  # Ensure proper cleanup on close
    root.mainloop()

if __name__ == "__main__":
    create_gui()
