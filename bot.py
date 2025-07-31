import os
import requests
import datetime
import time
import json

BOT_TOKEN = os.environ["7565508743:AAGtHC_r4dC0btVRCiuWaJqOIGsjGjAXAmg"]
CHAT_ID = os.environ["5958794945"]
API_KEY = os.environ["880c928bca884bd887a021c0c24b8b5e"]
BASE_URL = "https://api.twelvedata.com"

VALID_SESSIONS = {
    "London": range(7, 16),
    "NY": range(13, 21),
    "Asia": range(23, 24)
}

def in_session():
    now_hour = datetime.datetime.utcnow().hour
    for hours in VALID_SESSIONS.values():
        if now_hour in hours:
            return True
    return False

R_ALERTS = {
    "xauusd": {
        "core": {
            "pair": "XAU/USD",
            "rsi": {"below": 43},
            "price": {"below": 3315.50},
            "candle_close": {"below": 3318}
        }
    },
    "btcusd": {
        "core": {
            "pair": "BTC/USD",
            "rsi": {"below": 44},
            "candle_close": {"below": 118640}
        }
    }
}

def send_alert(text):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")

def get_price(symbol):
    params = {"symbol": symbol, "interval": "1min", "apikey": API_KEY}
    r = requests.get(f"{BASE_URL}/time_series", params=params)
    data = r.json()
    try:
        close = float(data["values"][0]["close"])
        return close
    except:
        return None

def get_rsi(symbol):
    params = {"symbol": symbol, "interval": "1min", "apikey": API_KEY, "time_period": 14}
    r = requests.get(f"{BASE_URL}/rsi", params=params)
    data = r.json()
    try:
        rsi = float(data["values"][0]["rsi"])
        return rsi
    except:
        return None

sent_entries = set()
send_alert("🚀 Test Alert from Robbo — You’re locked in Tayto! 💥")

while True:
    if not in_session():
        print("⏳ Outside valid session. Waiting...")
        time.sleep(60)
        continue

    for symbol, entries in R_ALERTS.items():
        twelve_symbol = symbol.upper()
        price = get_price(twelve_symbol)
        rsi = get_rsi(twelve_symbol)

        if price is None or rsi is None:
            print(f"⚠️ Data fetch failed for {symbol}")
            continue

        for entry_name, entry in entries.items():
            alert_key = f"{symbol}_{entry_name}"
            triggered = False

            if "rsi" in entry and "below" in entry["rsi"] and rsi < entry["rsi"]["below"]:
                triggered = True
            if "price" in entry and "below" in entry["price"] and price < entry["price"]["below"]:
                triggered = True
            if "candle_close" in entry and "below" in entry["candle_close"] and price < entry["candle_close"]["below"]:
                triggered = True

            if triggered and alert_key not in sent_entries:
                alert_text = f"📡 Sniper Entry 🔫\nPair: {entry['pair']}\nPrice: {price:.2f} | RSI: {rsi:.1f}"
                send_alert(alert_text)
                sent_entries.add(alert_key)
                print(f"✅ Alert Sent: {alert_text}")
            else:
                print(f"❌ No signal for {entry['pair']} | Price: {price:.2f} | RSI: {rsi:.1f}")

    time.sleep(60)
