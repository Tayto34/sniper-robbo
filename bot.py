=== SNIPER ROBBO PHASE 4: FINAL BUILD ===

Features: Multi-Entry Logic, Session Filters, Real-Time Scanner, Twelve Data API Integration, Auto Telegram Alerts

import requests, datetime, time, json

=== SECRETS ===

BOT_TOKEN = "7565508743:AAGtHC_r4dCObtVRCiuWa..."  # Telegram Bot Token CHAT_ID = "5958794945"  # Your Telegram ID API_KEY = "880c928bca884bd887a021c0c24b8b5e"  # Twelve Data API Key BASE_URL = "https://api.twelvedata.com/time_series"

=== SESSIONS ===

VALID_SESSIONS = { "London": range(7, 16), "NY": range(12, 21), "Asia": list(range(0, 7)) + list(range(23, 24)) }

=== JSON SNIPER SETUPS (ALL PAIRS, ALL 3 ENTRY TYPES) ===

R_ALERTS = { "xauusd": { "core": {"pair": "XAU/USD", "type": "SELL ⬇️", "entry": 3324.50, "sl": 3329.80, "tp": 3313.00, "rsi": 55, "condition": "close < 3324.50"}, "retest": {"entry": 3328.00, "sl": 3332.00, "tp": 3315.00, "rsi": 50, "condition": "close == 3328.00"}, "extension": {"entry": 3315.00, "sl": 3319.50, "tp": 3304.00, "rsi": 45, "condition": "close < 3315.00"} }, "us30": { "core": {"pair": "US30", "type": "BUY ⬆️", "entry": 44916, "sl": 44850, "tp": 45030, "rsi": 50, "condition": "close > 44916"}, "retest": {"entry": 44880, "sl": 44820, "tp": 44980, "rsi": 48, "condition": "close == 44880"}, "extension": {"entry": 45050, "sl": 44990, "tp": 45180, "rsi": 55, "condition": "close > 45050"} }, "btcusd": { "core": {"pair": "BTC/USD", "type": "BUY ⬆️", "entry": 118500, "sl": 118100, "tp": 119400, "rsi": 44, "condition": "close > 118500"}, "retest": {"entry": 118300, "sl": 117900, "tp": 119000, "rsi": 40, "condition": "close == 118300"}, "extension": {"entry": 118900, "sl": 118500, "tp": 119800, "rsi": 48, "condition": "close > 118900"} }, "eurusd": { "core": {"pair": "EUR/USD", "type": "SELL ⬇️", "entry": 1.15650, "sl": 1.15880, "tp": 1.15100, "rsi": 43, "condition": "close < 1.15650"}, "retest": {"entry": 1.15780, "sl": 1.16000, "tp": 1.15300, "rsi": 45, "condition": "close == 1.15780"}, "extension": {"entry": 1.15500, "sl": 1.15730, "tp": 1.14900, "rsi": 42, "condition": "close < 1.15500"} }, "gbpusd": { "core": {"pair": "GBP/USD", "type": "BUY ⬆️", "entry": 1.3360, "sl": 1.3330, "tp": 1.3440, "rsi": 60, "condition": "close > 1.3360"}, "retest": {"entry": 1.3340, "sl": 1.3315, "tp": 1.3400, "rsi": 58, "condition": "close == 1.3340"}, "extension": {"entry": 1.3385, "sl": 1.3360, "tp": 1.3460, "rsi": 62, "condition": "close > 1.3385"} } }

=== HELPERS ===

def send_alert(text): requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": text})

def get_price(pair): params = {"symbol": pair, "interval": "1min", "apikey": API_KEY, "outputsize": 1} res = requests.get(BASE_URL, params=params) try: data = res.json()["values"][0] return float(data["close"]), float(data["rsi"]) except: return None, None

def in_session(): now_hour = datetime.datetime.utcnow().hour for session, hours in VALID_SESSIONS.items(): if now_hour in hours: return True return False

=== MAIN LOOP ===

sent_entries = set() while True: if not in_session(): time.sleep(60) continue

for symbol, entries in R_ALERTS.items():
    twelve_symbol = symbol.upper()
    price, rsi = get_price(twelve_symbol)
    if price is None:
        continue

    for entry_type, config in entries.items():
        if entry_type + symbol in sent_entries:
            continue

        condition_met = eval(config["condition"].replace("close", str(price))) and rsi >= config["rsi"]
        if condition_met:
            msg = f"🚨 SNIPER ALERT [{entry_type.upper()}] 🚨\nPair: {config['pair']}\nType: {config['type']}\nEntry: {config['entry']}\nSL: {config['sl']}\nTP: {config['tp']}\nRSI: {rsi:.2f}"
            send_alert(msg)
            sent_entries.add(entry_type + symbol)

time.sleep(60)

