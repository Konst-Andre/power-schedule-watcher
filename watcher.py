import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://www.uz.gov.ua/about/activity/electropostachannia/electro_consumers/temporary_shutdown/grafikiobmezhen/622248/"
QUEUE = "4.1"

TELEGRAM_TOKEN = os.getenv("7745807427:AAHQla-yWeFh3PkxcfzACfaH-wb7Jk2ZEyM")
CHAT_ID = os.getenv("378886424")

HEADERS = {"User-Agent": "Mozilla/5.0"}

def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except:
        pass

def fetch():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=20)
        return r.text
    except Exception as e:
        print("Fetch error:", e)
        return None

send("🤖 Power Watcher запущено")

last = None

while True:
    html = fetch()

    if html:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)

        if QUEUE in text:
            if last and text != last:
                send("⚡ ЗМІНИ У ГРАФІКУ для черги 4.1")
            last = text

    time.sleep(60 * 60 * 3)

