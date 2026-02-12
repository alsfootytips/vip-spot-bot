import requests
import time
import os

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

URL = "https://mymembers.io/alsfootytipsvip"
FULL_TEXT = "There are no spots left for this page"


def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message},
        timeout=10
    )


def get_state():
    response = requests.get(URL, timeout=10)
    content = response.text
    if FULL_TEXT in content:
        return "full"
    return "open"


print("VIP spots monitor running...")

# Detect actual starting state
current_state = get_state()
print(f"Starting state: {current_state}")

while True:
    try:
        new_state = get_state()

        # VIP spots just opened
        if current_state == "full" and new_state == "open":
            send_telegram(
                "🚨 VIP SPOTS JUST OPENED!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
            )
            print("VIP spots opened alert sent.")

        # VIP spots just taken
        if current_state == "open" and new_state == "full":
            send_telegram(
                "❌ VIP spots have now been taken."
            )
            print("VIP spots taken alert sent.")

        current_state = new_state

    except Exception as e:
        print("Error:", e)

    time.sleep(30)
