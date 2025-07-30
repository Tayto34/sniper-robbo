from telegram import Bot
from telegram.ext import Application, CommandHandler
import requests
import asyncio
import logging

from config import TELEGRAM_TOKEN, TELEGRAM_USER_ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Sniper Message Sender
async def send_sniper_alert(context):
    message = "🚨 SNIPER ENTRY ALERT 🚨\n\nPair: XAU/USD\nType: SELL\nZone: 3321.50 broken\nTimeframe: 15m\nRSI: 43"
    await context.bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)

# /start Command
async def start(update, context):
    await update.message.reply_text("🔫 Robbo Sniper Bot Activated.\nReady to hunt entries, boss.")

# /test Command
async def test_alert(update, context):
    await update.message.reply_text("📡 Sending test sniper alert...")
    await send_sniper_alert(context)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_alert))

    # Optional: You can run alerts periodically if needed
    # app.job_queue.run_repeating(send_sniper_alert, interval=60, first=10)

    print("🤖 Robbo Sniper Bot is live.")
    app.run_polling()

if __name__ == '__main__':
    main()
