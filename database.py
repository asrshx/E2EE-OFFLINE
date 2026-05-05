# database.py ke andar simple JSON config
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

DEFAULT_CONFIG = {
    'MAIN': {
        'chat_id': 'TERA_CHAT_ID',
        'name_prefix': '[END TO END]',
        'delay': 10,
        'cookies': 'TERI_COOKIES',
        'messages': 'Hello\nHi\nKya haal hai'
    }
}

def get_user_config(user_id):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            data = json.load(f)
        return data.get(user_id, DEFAULT_CONFIG.get(user_id))
    return DEFAULT_CONFIG.get(user_id, None)

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    data = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            data = json.load(f)
    data[user_id] = {
        'chat_id': chat_id,
        'name_prefix': name_prefix,
        'delay': delay,
        'cookies': cookies,
        'messages': messages
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def set_automation_running(user_id, status):
    pass  # JSON ke saath zaroorat nahi
