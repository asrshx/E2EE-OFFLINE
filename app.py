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

import streamlit as st

# Is line ke pehle koi space nahi hona chahiye
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(160deg, #1a0033 0%, #4a0033 50%, #2d004d 100%);
}

/* Main Container Card */
.main .block-container {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px !important;
    padding: 20px !important;
    margin: 20px auto !important;
    border: 1px solid rgba(255, 105, 180, 0.25) !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4) !important;
    max-width: 420px !important;
}

/* Rounded Header Image 150x80 */
.custom-header {
    width: 150px !important;
    height: 80px !important;
    object-fit: cover;
    border-radius: 15px;
    display: block;
    margin: 0 auto 15px auto;
    border: 2px solid #ff69b4;
}

h1, h2, h3, p, label {
    color: white !important;
    text-align: center;
}

.stTextInput>div>div>input {
    background: rgba(0, 0, 0, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: white !important;
}

.stButton>button {
    background: linear-gradient(90deg, #ff0080, #7928ca) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    width: 100% !important;
    font-weight: 700 !important;
    padding: 10px !important;
}

footer, header {visibility: hidden;}
</style>
"""

# Streamlit code example:
import streamlit as st

st.markdown(custom_css, unsafe_allow_html=True)

# Pura content ishi sequence mein card ke andar dikhega
st.markdown('<img src="YOUR_IMAGE_LINK_HERE" class="custom-image">', unsafe_allow_html=True)
st.markdown("### Welcome to My App")
st.write("Ye pura content ab ek hi aesthetic card ke andar hai.")
name = st.text_input("Apna Naam Likhein")
if st.button("Click Me"):
    st.success(f"Hello {name}!")

# Streamlit me image dikhane ke liye ye tarika use karein:
# st.markdown(f'<img src="YOUR_IMAGE_URL" class="custom-image">', unsafe_allow_html=True)

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
st.markdown("""
<div class="main-header">
    <img src="https://i.imgur.com/KyCJzk9.jpeg" class="header-logo"
         onerror="this.style.display='none'">
    <h1>E2EE</h1>
    <p>seven billion smiles in this world but yours is my favourite ___</p>
</div>
""", unsafe_allow_html=True)

user_config = db.get_user_config('MAIN')

if user_config:
    tab1, tab2 = st.tabs(["Configuration", "Automation"])

    with tab1:
        st.markdown("### Your Configuration")

        chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'],
                               placeholder="e.g., 1362400298935018",
                               help="Facebook conversation ID from the URL")

        name_prefix = st.text_input("Name Prefix", value=user_config['name_prefix'],
                                   placeholder="e.g., [END TO END]",
                                   help="Prefix to add before each message")

        delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                               value=user_config['delay'],
                               help="Wait time between messages")

        cookies = st.text_area("Facebook Cookies (optional)",
                              value="",
                              placeholder="Paste your Facebook cookies here",
                              height=100,
                              help="Your cookies are stored encrypted")

        messages = st.text_area("Messages (one per line)",
                               value=user_config['messages'],
                               placeholder="Paste your messages here, one per line",
                               height=150,
                               help="Enter each message on a new line")

        if st.button("Save Configuration", use_container_width=True):
            final_cookies = cookies if cookies.strip() else user_config['cookies']
            db.update_user_config(
                'MAIN',
                chat_id,
                name_prefix,
                delay,
                final_cookies,
                messages
            )
            st.success("Configuration saved successfully!")
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
st.markdown('<div class="footer">Made with love by HENRY-- | 2025</div>', unsafe_allow_html=True)
