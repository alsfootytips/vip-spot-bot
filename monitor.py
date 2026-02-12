import requests
import time
import os

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"


URL = "https://mymembers.io/alsfootytipsvip"
FULL_TEXT = "There are no spots left for this page"

alert_sent = False


def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message},
        timeout=10
    )


print("VIP spot monitor running...")

while True:
    try:
        response = requests.get(URL, timeout=10)
        content = response.text

        # Case 1: Page says FULL
        if FULL_TEXT in content:
            alert_sent = False
            print("Still full – no alert.")

        # Case 2: Page no longer says FULL → spot open
        else:
            if not alert_sent:
                send_telegram(
                    "🚨 VIP SPOT JUST OPENED!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
                )
                print("Alert sent!")
                alert_sent = True

    except Exception as e:
        print("Error:", e)

    time.sleep(30)
