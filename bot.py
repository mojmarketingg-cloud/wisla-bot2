import os
import asyncio
from telegram import Bot
from playwright.async_api import async_playwright

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://bilety.wislakrakow.com/Stadium/Index?eventId=9903"

async def check_tickets():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = await browser.new_page()
        await page.goto(URL, timeout=60000)

        content = await page.content()

        await browser.close()

        return "Brak miejsc" not in content


async def main():
    bot = Bot(token=TOKEN)

    while True:
        try:
            available = await check_tickets()

            if available:
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text="🔥 BILETY DOSTĘPNE !!! 🔥\nhttps://bilety.wislakrakow.com"
                )
                await asyncio.sleep(300)

            else:
                print("Brak biletów...")
                await asyncio.sleep(20)

        except Exception as e:
            print("ERROR:", e)
            await asyncio.sleep(60)


asyncio.run(main())
