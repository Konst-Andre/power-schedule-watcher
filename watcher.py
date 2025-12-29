import requests
from bs4 import BeautifulSoup
import json, time

URL = "https://www.uz.gov.ua/about/activity/electropostachannia/electro_consumers/temporary_shutdown/grafikiobmezhen/622248/"
CHECK_INTERVAL = 60 * 60 * 3  # 3 години
STATE_FILE = "state.json"

BOT_TOKEN = "7745807427:AAHQla-yWeFh3PkxcfzACfaH-wb7Jk2ZEyM"
CHAT_ID = 378886424

def get_page():
    return requests.get(URL, timeout=30).text

def parse_4_1(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    result = {}

    for row in table.find_all("tr"):
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if cols and "4.1. черга" in cols[0].lower():
            date, time_range = cols[1], cols[2]
            result.setdefault(date, []).append(time_range)

    return result

def notify(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def load_state():
    try:
        return json.load(open(STATE_FILE))
    except:
        return {}

def save_state(data):
    json.dump(data, open(STATE_FILE, "w"))

while True:
    old = load_state()
    new = parse_4_1(get_page())

    if new != old:
        notify(f"⚡ Оновлення графіка 4.1:\n{new}")
        save_state(new)

    time.sleep(CHECK_INTERVAL)
