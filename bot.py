import requests
import time
import os
import re
from bs4 import BeautifulSoup
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

last_count = None
daily_start = None


def get_tickets():
    try:
        url = "https://bilety.wislakrakow.com/"
        r = requests.get(url, timeout=20)

        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()

        match = re.search(r"Sprzedane bilety:\s*(\d+)", text)

        if match:
            return int(match.group(1))

    except:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ Błąd pobierania danych!")

    return None


def hourly_check():
    global last_count

    count = get_tickets()

    if count is None:
        return

    if last_count is None:
        last_count = count
        return

    diff = count - last_count

    if diff > 0:
        message = f"""
🔥 SPRZEDAŻ ROŚNIE!

🎟 Sprzedane: {count}
📈 Ostatnia godzina: +{diff}
"""
    else:
        message = f"""
😴 Brak nowych biletów.

🎟 Nadal: {count}
"""

    bot.send_message(chat_id=CHAT_ID, text=message)

    last_count = count


def daily_report():
    global daily_start

    count = get_tickets()

    if count is None or daily_start is None:
        return

    sold_today = count - daily_start

    bot.send_message(
        chat_id=CHAT_ID,
        text=f"""
📊 PODSUMOWANIE DNIA

🔥 Sprzedano dziś: {sold_today}
🎟 Łącznie: {count}
"""
    )

    daily_start = count


def start_bot():
    global last_count, daily_start

    count = get_tickets()

    last_count = count
    daily_start = count

    bot.send_message(
        chat_id=CHAT_ID,
        text=f"""
✅ BOT WYSTARTOWAŁ!

🎟 Aktualnie sprzedane: {count}

⏰ Sprawdzam co godzinę.
📊 Raport o 23:00.
"""
    )


scheduler = BlockingScheduler()

scheduler.add_job(start_bot, "date")
scheduler.add_job(hourly_check, "interval", hours=1)
scheduler.add_job(daily_report, "cron", hour=23)

scheduler.start()
