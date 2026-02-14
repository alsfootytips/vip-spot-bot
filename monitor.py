import time
import requests
from playwright.sync_api import sync_playwright

# =========================
# CONFIG
# =========================
URL = "https://mymembers.io/alsfootytipsvip"

BOT_TOKEN = "8518789928:AAGEx1Fo7mzm_31EtcGe8yyS1rLrDxA7YoU"
CHAT_ID = "-1002856575590"

CHECK_INTERVAL = 25  # seconds between checks
REQUIRED_OPEN_CHECKS = 2  # how many consecutive "open" checks needed


# =========================
# TELEGRAM FUNCTION
# =========================
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False,
    }
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


# =========================
# PAGE CHECK FUNCTION
# =========================
def check_page_state(page):
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(4000)  # wait for JS to render

    content = page.content().lower()

    if "no spots left" in content:
        return "full"

    if "spots left" in content or "buy now" in content:
        return "open"

    # fallback
    return "unknown"


# =========================
# MAIN LOOP
# =========================
def main():
    print("VIP spots monitor running...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        current_state = check_page_state(page)
        print("Starting state:", current_state)

        open_counter = 0

        while True:
            try:
                new_state = check_page_state(page)
                print(f"Current: {current_state} | New: {new_state}")

                # ======================
                # OPEN DETECTION
                # ======================
                if new_state == "open":
                    open_counter += 1
                else:
                    open_counter = 0

                if (
                    open_counter >= REQUIRED_OPEN_CHECKS
                    and current_state == "full"
                ):
                    send_telegram(
                        "🚨 VIP SPOTS JUST OPENED!\n\nJoin now:\nhttps://mymembers.io/alsfootytipsvip"
                    )
                    current_state = "open"
                    open_counter = 0

                # ======================
                # FULL DETECTION
                # ======================
                if new_state == "full" and current_state == "open":
                    send_telegram("❌ VIP spots have now been taken.")
                    current_state = "full"
                    open_counter = 0

            except Exception as e:
                print("Error:", e)

            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
