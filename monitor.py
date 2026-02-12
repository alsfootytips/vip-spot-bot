import requests
import time
import os

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

URL = "https://mymembers.io/alsfootytipsvip"
KEYWORD = "SPOTS LEFT"

def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message}
    )

print("Bot started...")

while True:
    try:
        response = requests.get(URL, timeout=10)
        content = response.text

        if KEYWORD in content:
            send_telegram("🚨 VIP spot just opened! Join now:")
            send_telegram(URL)
            print("Alert sent!")
            time.sleep(300)  # wait 5 mins after alert
        else:
            print("No spots yet.")

    except Exception as e:
        print("Error:", e)

    time.sleep(30)  # check every 30 seconds

