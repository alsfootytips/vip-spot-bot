import time
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

URL = "https://mymembers.io/alsfootytipsvip"
FULL_TEXT = "There are no spots left for this page"

current_state = None


def send_telegram(message):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message},
        timeout=10,
    )


def check_page(browser):
    page = browser.new_page()
    page.goto(URL, timeout=30000)
    page.wait_for_timeout(3000)  # wait for JS to render
    content = page.content()
    page.close()
    return content


print("VIP spots monitor running...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    while True:
        try:
            content = check_page(browser)

            if FULL_TEXT in content:
                new_state = "full"
            else:
                new_state = "open"

            if current_state is None:
                current_state = new_state
                print("Starting state:", current_state)

            elif current_state == "full" and new_state == "open":
                send_telegram(
                    "🚨 VIP SPOTS JUST OPENED!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
                )
                print("VIP spots opened alert sent.")

            elif current_state == "open" and new_state == "full":
                send_telegram("❌ VIP spots have now been taken.")
                print("VIP spots taken alert sent.")

            current_state = new_state

        except Exception as e:
            print("Error:", e)

        time.sleep(30)
