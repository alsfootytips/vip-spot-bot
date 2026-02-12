import requests
import time
import os

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

URL = "https://mymembers.io/alsfootytipsvip"

alert_sent = False  # prevents duplicate alerts


def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message},
    )


print("Bot started...")

while True:
    try:
        response = requests.get(URL, timeout=10)
        content = response.text.lower()

        # Detect if spots are available
        if "spots left" in content and not alert_sent:
            send_telegram(
                "🚨 VIP spot just opened!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
            )
            print("Alert sent!")
            alert_sent = True

        # Reset if page shows no spots
        if "spots left" not in content:
            alert_sent = False
            print("No spots available.")

    except Exception as e:
        print("Error:", e)

    time.sleep(30)  # checks every 30 seconds
