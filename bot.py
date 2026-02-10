import asyncio
from playwright.async_api import async_playwright
import requests
import os
import json
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bilety.wislakrakow.com/Stadium/Index?eventId=9903"
DATA_FILE = "data.json"


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )


async def get_tickets():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()

        await page.goto(URL, timeout=60000)
        await page.wait_for_timeout(6000)

        text = await page.inner_text("body")

        await browser.close()

        import re
        match = re.search(r"Sprzedane bilety:\s*(\d+)", text)

        if match:
            return int(match.group(1))
        return None


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def calc_growth(data, hours):
    cutoff = datetime.now() - timedelta(hours=hours)

    for record in reversed(data):
        if datetime.fromisoformat(record["time"]) <= cutoff:
            return data[-1]["count"] - record["count"]

    return 0


async def main():
    now_count = await get_tickets()

    if now_count is None:
        send("❌ Nie udało się pobrać liczby biletów")
        return

    data = load_data()

    data.append({
        "time": datetime.now().isoformat(),
        "count": now_count
    })

    save_data(data)

    hour_growth = calc_growth(data, 1)
    day_growth = calc_growth(data, 24)

    msg = f"""
🎟 Sprzedane bilety: {now_count}

📈 Ostatnia godzina: +{hour_growth}
🔥 Ostatnie 24h: +{day_growth}
"""

    send(msg)


asyncio.run(main())
