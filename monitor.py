import requests
import time

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

URL = "https://mymembers.io/alsfootytipsvip"

current_state = None  # will be set after first check


def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message},
        timeout=10
    )


print("VIP spots monitor running...")

while True:
    try:
        response = requests.get(URL, timeout=10)
        content = response.text.lower()

        # Detect state
        if "no spots left" in content:
            new_state = "full"
        else:
            new_state = "open"

        # Set initial state without sending message
        if current_state is None:
            current_state = new_state
            print("Starting state:", current_state)

        # VIP spots just opened
        elif current_state == "full" and new_state == "open":
            send_telegram(
                "🚨 VIP SPOTS JUST OPENED!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
            )
            print("VIP spots opened alert sent.")
            current_state = new_state

        # VIP spots just taken
        elif current_state == "open" and new_state == "full":
            send_telegram("❌ VIP spots have now been taken.")
            print("VIP spots taken alert sent.")
            current_state = new_state

        else:
            current_state = new_state
            print("No change. Current state:", current_state)

    except Exception as e:
        print("Error:", e)

    time.sleep(30)
