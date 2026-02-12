import requests
import time

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

URL = "https://mymembers.io/alsfootytipsvip"

current_state = None  # unknown at start


def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message},
        timeout=10
    )


def get_state():
    response = requests.get(URL, timeout=10)
    content = response.text.lower()

    print("---- PAGE CHECK ----")
    print("Contains 'spots left':", "spots left" in content)
    print("Contains 'no spots':", "no spots" in content)
    print("--------------------")

    if "spots left" in content:
        return "open"
    else:
        return "full"


print("VIP spots monitor running...")

current_state = get_state()
print(f"Starting state: {current_state}")

while True:
    try:
        new_state = get_state()
        print(f"Current: {current_state} | New: {new_state}")

        # Spots just opened
        if current_state == "full" and new_state == "open":
            send_telegram(
                "🚨 VIP SPOTS JUST OPENED!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
            )
            print("OPEN alert sent")

        # Spots just taken
        if current_state == "open" and new_state == "full":
            send_telegram("❌ VIP spots have now been taken.")
            print("FULL alert sent")

        current_state = new_state

    except Exception as e:
        print("Error:", e)

    time.sleep(30)
