import requests
import time
import hashlib
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ====== CONFIG ======

URL = "https://www.uz.gov.ua/about/activity/electropostachannia/electro_consumers/temporary_shutdown/grafikiobmezhen/622248/"
TELEGRAM_TOKEN = os.getenv("7745807427:AAHQla-yWeFh3PkxcfzACfaH-wb7Jk2ZEyM")
CHAT_ID = os.getenv("378886424")
CHECK_INTERVAL = 60 * 60 * 3   # 3 години

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ====== TELEGRAM ======

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

# ====== NETWORK SESSION ======

session = requests.Session()

retry = Retry(
    total=5,
    backoff_factor=10,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

# ====== STATE ======

last_hash = ""

# ====== MAIN LOOP ======

while True:
    try:
        response = session.get(URL, headers=HEADERS, timeout=60)
        html = response.text

        current_hash = hashlib.md5(html.encode()).hexdigest()

        if current_hash != last_hash:
            last_hash = current_hash
            send_message("⚡️ Графік відключень оновився! Перевіряй сайт УЗ.")

        else:
            print("No changes")

    except Exception as e:
        print("Ukrzaliznytsia unreachable:", e)

    time.sleep(CHECK_INTERVAL)
