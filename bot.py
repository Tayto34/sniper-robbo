from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔐 Telegram bot token
TELEGRAM_BOT_TOKEN = "7565508743:AAGtHC_r4dC0btVRCiuWaJqOIGsjGjAXAmg"

# 🎯 Sniper Entry Templates with Multi-Entry Logic
R_ALERTS = {
    "xauusd": {
        "core": {
            "pair": "XAU/USD",
            "type": "SELL 🔻",
            "entry": "3324.50",
            "sl": "3329.80",
            "tp": "3313.00",
            "risk": "1%",
            "reason": "RSI below 43 + 15m close under 3324",
        },
        "retest": {
            "entry": "3326.00",
            "sl": "3330.50",
            "tp": "3315.00",
            "risk": "0.5%",
            "reason": "Retest entry after rejection at resistance",
        },
        "momentum": {
            "entry": "3322.00",
            "sl": "3326.00",
            "tp": "3311.00",
            "risk": "0.5%",
            "reason": "Momentum continuation on strong bearish candle",
        }
    },
    "btc": {
        "core": {
            "pair": "BTC/USD",
            "type": "BUY 🔼",
            "entry": "117850",
            "sl": "117720",
            "tp": "118200",
            "risk": "1%",
            "reason": "Liquidity sweep + RSI above 40",
        }
    }
}

# 📊 Accuracy Tracking Placeholder
TRACKER = []

# 📌 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🟢 Robbo Sniper Bot Activated.\nUse /test or /fire to launch signals."
    )

# 📌 /test command
async def test_alert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🧪 Sending test sniper alert...")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🚨 SNIPER ENTRY ALERT 🚨\nThis is a test.")

# 📌 /fire command
async def fire_alert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for symbol, entries in R_ALERTS.items():
        for entry_type, data in entries.items():
            msg = (
                f"🚨 SNIPER ENTRY [{entry_type.upper()}] 🚨\n\n"
                f"📌 Pair: {data['pair']}\n"
                f"📈 Type: {data['type'] if 'type' in data else 'SELL/BUY'}\n"
                f"🎯 Entry: {data['entry']}\n"
                f"🛑 SL: {data['sl']}\n"
                f"✅ TP: {data['tp']}\n"
                f"💰 Risk: {data['risk']}\n\n"
                f"📖 Reason: {data['reason']}"
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

# 📌 /track command to log results (placeholder)
async def track_alert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args and len(context.args) == 4:
        pair, entry_type, result, rr = context.args
        TRACKER.append({"pair": pair, "entry": entry_type, "result": result, "rr": rr})
        await update.message.reply_text(f"✅ Logged: {pair} | {entry_type} | {result.upper()} | RR: {rr}")
    else:
        await update.message.reply_text("Usage: /track XAU/USD core win 2.5")

# 🛡️ Fallback handler for any other message
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⚠️ Robbo only responds to commands like /start, /fire, /test, /track")

# 🧠 Main
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_alert))
    app.add_handler(CommandHandler("fire", fire_alert))
    app.add_handler(CommandHandler("track", track_alert))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Robbo Sniper Bot locked and loaded.")
    app.run_polling()

if __name__ == "__main__":
    main()
