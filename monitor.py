import requests
import time

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

URL = "https://mymembers.io/alsfootytipsvip"
FULL_TEXT = "no spots left for this page"

current_state = None  # will be set on first check


def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message},
        timeout=10
    )


print("VIP spots monitor running...")

# Detect starting state
try:
    response = requests.get(URL, timeout=10)
    content = response.text.lower()

    if FULL_TEXT in content:
        current_state = "full"
    else:
        current_state = "open"

    print("Starting state:", current_state)

except Exception as e:
    print("Startup error:", e)
    current_state = "full"


while True:
    try:
        response = requests.get(URL, timeout=10)
        content = response.text.lower()

        if FULL_TEXT in content:
            new_state = "full"
        else:
            new_state = "open"

        # Spots just opened
        if current_state == "full" and new_state == "open":
            send_telegram(
                "🚨 VIP SPOTS JUST OPENED!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
            )
            print("VIP spots opened alert sent.")

        # Spots just taken
        if current_state == "open" and new_state == "full":
            send_telegram("❌ VIP spots have now been taken.")
            print("VIP spots taken alert sent.")

        current_state = new_state

    except Exception as e:
        print("Error:", e)

    time.sleep(30)
