import requests
import time
import os

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

URL = "https://mymembers.io/alsfootytipsvip"
FULL_TEXT = "THIS TEXT DOES NOT EXIST!"

def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message}
    )

print("Bot started...")

last_state = "full"

while True:
    try:
        response = requests.get(URL, timeout=10)
        content = response.text

        if FULL_TEXT in content:
            state = "full"
            print("No spots available.")
        else:
            state = "open"
            print("Spots might be open!")

        # Send alert only when state changes from full → open
        if last_state == "full" and state == "open":
            send_telegram(
                "🚨 VIP SPOT JUST OPENED!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
            )
            print("Alert sent!")

        last_state = state

    except Exception as e:
        print("Error:", e)

    time.sleep(60)  # check every 60 seconds
