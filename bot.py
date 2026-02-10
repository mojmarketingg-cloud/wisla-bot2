import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

bilety = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot działa ✅")

async def pokaz_licznik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    count = bilety.get(user_id, 0)
    await update.message.reply_text(f"Masz {count} biletów 🎫")

async def dodaj_bilet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bilety[user_id] = bilety.get(user_id, 0) + 1
    await update.message.reply_text("Dodano bilet 🎫")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("licznik", pokaz_licznik))
app.add_handler(CommandHandler("bilet", dodaj_bilet))

app.run_polling(drop_pending_updates=True)
