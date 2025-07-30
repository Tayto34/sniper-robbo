from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔐 Replace with your actual bot token
TELEGRAM_BOT_TOKEN = "7565508743:AAGtHC_r4dC0btVRCiuWaJqOIGsjGjAXAmg"

# 🎯 Sniper JSON templates
R_ALERTS = {
    "xauusd": {
        "pair": "XAU/USD",
        "direction": "SELL 🔻",
        "entry": "3324.50",
        "sl": "3329.80",
        "tp": "3313.00",
        "reason": "RSI below 43 + 15m close under 3320.70",
    },
    "btcusd": {
        "pair": "BTC/USD",
        "direction": "BUY 🟢",
        "entry": "117,990.00",
        "sl": "117,850.00",
        "tp": "118,700.00",
        "reason": "RSI above 44 + bullish candle close above 118,500",
    },
    "us30": {
        "pair": "US30",
        "direction": "BUY 🟢",
        "entry": "44,800.00",
        "sl": "44,700.00",
        "tp": "44,950.00",
        "reason": "15m bullish close above 44,916 + RSI back above 50",
    }
}

# 🚀 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Robbo Sniper Bot Active. Type /test to simulate alert.")

# 🧪 /test command
async def test_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧪 Sending test sniper alert...")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🚨 SNIPER ENTRY ALERT 🚨\nThis is a test."
    )

# 🔥 /fire command (sends real template)
async def fire_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        alert = R_ALERTS["xauusd"]
        message = (
            f"🚨 SNIPER ENTRY ALERT 🚨\n\n"
            f"Pair: {alert['pair']}\n"
            f"Direction: {alert['direction']}\n"
            f"Entry: {alert['entry']}\n"
            f"SL: {alert['sl']}\n"
            f"TP: {alert['tp']}\n\n"
            f"🧠 Reason: {alert['reason']}"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {e}")

# 💬 Respond to any other message
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Robbo only responds to commands like /start /test /fire")

# 🧠 Main runner
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 🔗 Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_alert))
    app.add_handler
