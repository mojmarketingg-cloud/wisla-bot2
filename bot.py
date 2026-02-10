import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

licznik = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot działa ✅")

async def pokaz_licznik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    count = licznik.get(user_id, 0)
    await update.message.reply_text(f"Wysłałeś {count} wiadomości 🙂")

async def licz_wiadomosci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    licznik[user_id] = licznik.get(user_id, 0) + 1

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("licznik", pokaz_licznik))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, licz_wiadomosci))

app.run_polling(drop_pending_updates=True)
