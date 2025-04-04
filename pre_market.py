
import os
import json
from datetime import datetime
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def generate_pre_market_message():
    today = datetime.now().strftime("%B %d, %Y")
    message = f"""📊 Pre-Market Overview — {today}

🌍 Global Macro:
- Nikkei down -2.7% on tariff fears
- ECB cuts rates 25bps — dovish tone
- CPI due at 8:30 AM ET — expected soft print

🧠 Sentiment Watch:
- Tech weakness likely if CPI surprises hot
- Safe haven flow to GC possible
- Oil reacting to geopolitical risk, eye on EIA report

🎯 Pre-Market Bias:
🟢 GC — Favor long above 2305
⚠️ ES — Wait for CPI confirmation
🔴 CL — Risk of breakdown below 84.50

Stay alert for CPI + Fed speak before open.
"""
    return message

def send_pre_market():
    msg = generate_pre_market_message()
    bot.send_message(chat_id=TELEGRAM_USER_ID, text=msg)

if __name__ == "__main__":
    send_pre_market()
