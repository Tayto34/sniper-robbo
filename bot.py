import requests
import datetime
import time
import json

# === SECRETS ===
BOT_TOKEN = "7565508743:AAGtHC_r4dC0btVRCiuWaJqOIGsjGjAXAmg"
CHAT_ID = "5958794945"
API_KEY = "880c928bca884bd887a021c0c24b8b5e"
BASE_URL = "https://api.twelvedata.com"

# === SESSION FILTER ===
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

# === SNIPER RULES (Edit for your own conditions) ===
R_ALERTS = {
    "xauusd": {
        "core": {
            "pair": "XAU/USD",
            "type": "Sniper Buy",
            "rsi_min": 60,
            "candle_close_above": 3318
        }
    },
    "us30": {
        "core": {
            "pair": "US30",
            "type": "Sniper Sell",
            "rsi_max": 45,
            "candle_close_below": 44950
        }
    }
}

# === HELPERS ===
def send_alert(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

def get_price(symbol):
    params = {"symbol": symbol, "interval": "15min", "apikey": API_KEY}
    rsi_url = f"{BASE_URL}/rsi"
    price_url = f"{BASE_URL}/time_series"
    rsi_res = requests.get(rsi_url, params=params).json()
    price_res = requests.get(price_url, params=params).json()
    rsi_value = float(rsi_res["values"][0]["rsi"])
    close_price = float(price_res["values"][0]["close"])
    return close_price, rsi_value

# === MAIN LOOP ===
sent_entries = set()

while True:
    if not in_session():
        print("⏳ Outside valid session. Waiting...")
        time.sleep(60)
        continue

    for symbol, entries in R_ALERTS.items():
        twelve_symbol = symbol.upper()
        price, rsi = get_price(twelve_symbol)

        for entry_type, entry in entries.items():
            pair = entry["pair"]
            alert_type = entry["type"]
            sent_id = f"{pair}_{entry_type}"

            if sent_id in sent_entries:
                continue

            passed = True

            if "rsi_min" in entry and rsi < entry["rsi_min"]:
                passed = False
            if "rsi_max" in entry and rsi > entry["rsi_max"]:
                passed = False
            if "candle_close_above" in entry and price <= entry["candle_close_above"]:
                passed = False
            if "candle_close_below" in entry and price >= entry["candle_close_below"]:
                passed = False

            if passed:
                msg = f"🔫 Sniper Alert\nPair: {pair}\nType: {alert_type}\nPrice: {price}\nRSI: {rsi:.2f}"
                send_alert(msg)
                print(f"✅ Alert Sent: {msg}")
                sent_entries.add(sent_id)
            else:
                print(f"❌ No signal for {pair} | Price: {price} | RSI: {rsi}")

    time.sleep(60)
