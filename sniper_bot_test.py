import requests
import datetime
import time
import json

# === SECRETS ===
BOT_TOKEN = "7565508743:AAGtHC_r4dCObtVRCiuWa..."  # Your Telegram bot token
CHAT_ID = "5958794945"  # Your Telegram chat ID
API_KEY = "880c928bca884bd887a021c0c24b8b5e"
BASE_URL = "https://api.twelvedata.com/time_series"

# === SESSIONS ===
VALID_SESSIONS = {
    "London": range(7, 16),
    "NY": range(12, 21),
    "Asia": list(range(0, 7)) + list(range(23, 24))
}

# === SNIPER ENTRY TEMPLATES ===
R_ALERTS = {
    "xauusd": {
        "core": {
            "pair": "XAU/USD", "type": "SELL", "entry": "3324.50",
            "sl": "3329.80", "tp": "3313.00",
            "reason": "RSI below 43 + 15m close under 3318"
        },
        "retest": {
            "entry": "3327.00", "sl": "3330.00", "tp": "3312.00",
            "reason": "Failed retest at 3327"
        },
        "momentum": {
            "entry": "3317.00", "sl": "3320.00", "tp": "3305.00",
            "reason": "Strong breakout momentum"
        },
        "reversal": {
            "entry": "3301.50", "sl": "3304.00", "tp": "3320.00",
            "reason": "15m candle rejection + RSI 20"
        }
    },
    "btcusd": {
        "core": {
            "pair": "BTC/USD", "type": "SELL", "entry": "118640",
            "sl": "118840", "tp": "117999",
            "reason": "15m close below 118640 + RSI < 44"
        },
        "retest": {
            "entry": "118700", "sl": "118950", "tp": "118100",
            "reason": "Break + retest structure"
        },
        "momentum": {
            "entry": "118500", "sl": "118650", "tp": "117600",
            "reason": "RSI oversold + dump candle"
        },
        "reversal": {
            "entry": "117999", "sl": "117800", "tp": "118900",
            "reason": "Fakeout + RSI divergence"
        }
    },
    "us30": {
        "core": {
            "pair": "US30", "type": "BUY", "entry": "44916",
            "sl": "44800", "tp": "45100",
            "reason": "15m breakout + RSI > 50"
        },
        "retest": {
            "entry": "44860", "sl": "44780", "tp": "45050",
            "reason": "Retest of broken zone"
        },
        "momentum": {
            "entry": "45010", "sl": "44890", "tp": "45290",
            "reason": "Volume spike + strong trend"
        },
        "reversal": {
            "entry": "44700", "sl": "44600", "tp": "45000",
            "reason": "Double bottom + RSI > 30"
        }
    },
    "ustec": {
        "core": {
            "pair": "USTEC", "type": "BUY", "entry": "23485",
            "sl": "23380", "tp": "23680",
            "reason": "15m confirmation above resistance"
        },
        "retest": {
            "entry": "23450", "sl": "23360", "tp": "23600",
            "reason": "Retest structure"
        },
        "momentum": {
            "entry": "23590", "sl": "23460", "tp": "23810",
            "reason": "Strong candle follow-through"
        },
        "reversal": {
            "entry": "23320", "sl": "23240", "tp": "23550",
            "reason": "W-bottom + RSI recovery"
        }
    },
    "gbpusd": {
        "core": {
            "pair": "GBP/USD", "type": "BUY", "entry": "1.3360",
            "sl": "1.3330", "tp": "1.3410",
            "reason": "Bullish engulf + RSI > 60"
        },
        "retest": {
            "entry": "1.3345", "sl": "1.3325", "tp": "1.3385",
            "reason": "Retest of resistance"
        },
        "momentum": {
            "entry": "1.3375", "sl": "1.3345", "tp": "1.3430",
            "reason": "Momentum continuation"
        },
        "reversal": {
            "entry": "1.3310", "sl": "1.3290", "tp": "1.3370",
            "reason": "RSI recovery from 30"
        }
    },
    "usdjpy": {
        "core": {
            "pair": "USD/JPY", "type": "BUY", "entry": "148.60",
            "sl": "148.30", "tp": "149.20",
            "reason": "RSI > 55 + breakout"
        },
        "retest": {
            "entry": "148.50", "sl": "148.20", "tp": "149.00",
            "reason": "Retest structure"
        },
        "momentum": {
            "entry": "148.85", "sl": "148.55", "tp": "149.70",
            "reason": "Strong impulse candle"
        },
        "reversal": {
            "entry": "148.10", "sl": "147.80", "tp": "148.90",
            "reason": "Oversold + engulfing candle"
        }
    },
    "eurusd": {
        "core": {
            "pair": "EUR/USD", "type": "SELL", "entry": "1.15650",
            "sl": "1.15800", "tp": "1.15200",
            "reason": "15m candle close below support + RSI < 43"
        },
        "retest": {
            "entry": "1.15780", "sl": "1.15900", "tp": "1.15400",
            "reason": "Retest resistance zone"
        },
        "momentum": {
            "entry": "1.15550", "sl": "1.15700", "tp": "1.15080",
            "reason": "Bearish engulfing + RSI < 30"
        },
        "reversal": {
            "entry": "1.15180", "sl": "1.15350", "tp": "1.15720",
            "reason": "Rejection + RSI recovery"
        }
    }
}

# === HELPER ===
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
