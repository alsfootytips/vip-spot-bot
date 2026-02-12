import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://mymembers.io/alsfootytipsvip"
KEYWORD = "There are no spots left for this page"

last_state = True

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

while True:
    try:
        r = requests.get(URL, timeout=10)
        text = r.text.lower()

        if KEYWORD.lower() in text:
            current_state = True
        else:
            current_state = False

        if last_state and not current_state:
            send_telegram(
                "🚨 VIP SPOT JUST OPENED!\n\nJoin now before it fills:\nhttps://mymembers.io/alsfootytipsvip"
            )

        last_state = current_state

    except Exception as e:
        print("Error:", e)

    time.sleep(60)
