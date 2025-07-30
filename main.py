import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get your token from environment (works on Render)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 🔫 Sniper alert message
async def send_sniper_alert(context: ContextTypes.DEFAULT_TYPE):
    message = "🚨 SNIPER ENTRY ALERT 🚨\nLocked and loaded!"
    await context.bot.send_message(chat_id=context.job.chat_id, text=message)

# /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔫 Robbo Sniper Bot Active. Type /test to simulate alert.")

# /test Command
async def test_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧪 Sending test sniper alert...")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🚨 SNIPER ENTRY ALERT 🚨\nThis is a test.")

# Main runner
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_alert))

    print("✅ Robbo Sniper running...")
    app.run_polling()

if __name__ == "__main__":
    main()
