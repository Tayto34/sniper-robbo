import requests
import datetime
import time
import json

# === SECRETS ===
BOT_TOKEN = "7565508743:AAGtHC_r4dC0btVRCiuWaJqOIGsjGjAXAmg"
CHAT_ID = "5958794945"
API_KEY = "880c928bca884bd887a021c0c24b8b5e"
BASE_URL = "https://api.twelvedata.com/time_series"

# === SESSIONS ===
VALID_SESSIONS = {
    "London": range(7, 16),
    "NY": range(12, 21),
    "Asia": list(range(0, 7)) + list(range(23, 24))
}

# === SNIPER STRATEGY (TEST WITH XAU/USD ONLY) ===
R_ALERTS = {
    "xauusd": {
        "core": {
            "pair": "XAU/USD",
            "type": "Core 🔔",
            "entry": 1000.0,
            "sl": 1005.0,
            "tp": 995.0,
            "risk": 1.0,
            "reason": "Core sniper confirmation",
            "session": "London/NY/Asia",
            "rsi": 45,
            "candle": "bullish"
        }
    }
}

# === FUNCTIONS ===
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("❌ Telegram error:", e)

def is_valid_session(session_string):
    current_hour = datetime.datetime.utcnow().hour
    for sess in session_string.split("/"):
        if current_hour in VALID_SESSIONS.get(sess, []):
            return True
    return False

def fetch_price_data(symbol):
    params = {
        "symbol": symbol.upper(),
        "interval": "1min",
        "outputsize": 1,
        "apikey": API_KEY
    }
    try:
        r = requests.get(BASE_URL, params=params)
        data = r.json()
        candles = data["values"][0]
        return {
            "open": float(candles["open"]),
            "close": float(candles["close"]),
            "rsi": float(data.get("meta", {}).get("indicator", {}).get("rsi", 50))
        }
    except:
        return None

def get_sniper_alert(pair, strategy_type, price_data):
    alert = R_ALERTS[pair][strategy_type]

    if not is_valid_session(alert["session"]):
        return f"⏱️ Not valid session for {pair.upper()}"

    if alert["candle"] == "bullish" and price_data["close"] < price_data["open"]:
        return f"❌ Candle not bullish for {pair.upper()}"
    if alert["candle"] == "bearish" and price_data["close"] > price_data["open"]:
        return f"❌ Candle not bearish for {pair.upper()}"
    if price_data["rsi"] < alert["rsi"]:
        return f"⚠️ RSI too low ({price_data['rsi']}) for {pair.upper()}"

    return f"""
🚨 {alert['type']} Alert for {alert['pair']}
Entry: {alert['entry']}
SL: {alert['sl']} | TP: {alert['tp']}
Risk: {alert['risk']}%
Session: {alert['session']}
Reason: {alert['reason']}
"""

def execute_trade(alert):
    print(f"⚡ Executing trade for {alert['pair']} @ {alert['entry']} with SL {alert['sl']} / TP {alert['tp']}")
    return {
        "entry": alert["entry"],
        "sl": alert["sl"],
        "tp": alert["tp"],
        "result": "pending",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

def track_accuracy(pair, strategy, alert_data, execution):
    log_file = "sniper_accuracy_log.json"
    try:
        with open(log_file, 'r') as f:
            log = json.load(f)
    except:
        log = {}

    if pair not in log:
        log[pair] = []

    log[pair].append({
        "strategy": strategy,
        "entry": alert_data['entry'],
        "sl": alert_data['sl'],
        "tp": alert_data['tp'],
        "risk": alert_data['risk'],
        "session": alert_data['session'],
        "result": execution['result'],
        "timestamp": execution['timestamp']
    })

    with open(log_file, 'w') as f:
        json.dump(log, f, indent=2)

# === LOOP ===
if __name__ == "__main__":
    while True:
        for pair in R_ALERTS:
            symbol = R_ALERTS[pair]['core']['pair']
            price_info = fetch_price_data(symbol)

            if not price_info:
                print(f"⚠️ No price for {pair.upper()} – skipping.")
                continue

            for strategy in R_ALERTS[pair]:
                alert = R_ALERTS[pair][strategy]
                print(f"⏳ {pair.upper()} | {strategy.upper()} – scanning...")
                alert_msg = get_sniper_alert(pair, strategy, price_info)
                print(alert_msg)
                if "🚨" in alert_msg:
                    send_telegram_alert(alert_msg)
                    execution = execute_trade(alert)
                    track_accuracy(pair, strategy, alert, execution)

        time.sleep(60)  # loop every 60 seconds
