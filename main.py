import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters

# Get your token from environment (works on Render)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 🔫 Sniper alert message
async def send_sniper_alert(context: ContextTypes.DEFAULT_TYPE):
    message = "🚨 SNIPER ENTRY ALERT 🚨\nLocked and loaded!"
    await context.bot.send_message(chat_id=context.job.chat_id, text=message)

# /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔫 Robbo Sniper Bot Active. Type /test to simulate alert.")

# /test Command /fire.
# /fire Command
async def fire_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("templates/xauusd_sell.json") as f:
            alert = json.load(f)

        message = 
            f"🚨 SNIPER ENTRY ALERT 🚨\n\n"
            f"Pair: {alert['pair']}\n"
            f"Direction: {alert['direction']}\n"
            f"Entry: {alert['entry']}\n"
            f"SL: {alert['sl']}\n"
            f"TP: {alert['tp']}\n\n"
            f"Reason: {alert['reason']}"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"❌ Error: {e}")
async def test_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧪 Sending test sniper alert...")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🚨 SNIPER ENTRY ALERT 🚨\nThis is a test.")
# 💬 Handle any regular message
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚠️ Robbo only responds to commands like /start, /test, or /fire.\nType /fire to trigger the sniper alert from the JSON."
)
# Main runner
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_alert))
    app.add_handler(CommandHandler("fire", fire_alert))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_alert))
    app.add_handler(CommandHandler("fire", fire_alert))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Robbo Sniper running...")
    app.run_polling()

if __name__ == "__main__":
    main()
