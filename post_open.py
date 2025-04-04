
import os
import json
from datetime import datetime
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def generate_post_open_ideas():
    ideas = {
        "ES": {
            "bias": "🔴 Sell",
            "reason": "ES broke below 5260 after hot CPI — risk-off across equities",
            "entry": "5250.00",
            "stop": "5268.00",
            "target": "5210.00"
        },
        "NQ": {
            "bias": "🔴 Sell",
            "reason": "Heavy tech selling post open — NQ down -1.3% from Globex high",
            "entry": "18210.00",
            "stop": "18320.00",
            "target": "18030.00"
        },
        "GC": {
            "bias": "🟢 Buy",
            "reason": "Gold bouncing after CPI miss — safe haven bid returns",
            "entry": "2315.00",
            "stop": "2302.00",
            "target": "2345.00"
        }
    }
    return ideas

def format_trade_ideas(data):
    today = datetime.now().strftime("%B %d, %Y")
    message = f"📉 Confirmed Trade Ideas — {today}\n"
    for symbol, idea in data.items():
        message += f"\n{idea['bias']} {symbol}\n"
        message += f" - Reason: {idea['reason']}\n"
        message += f" - Entry: {idea['entry']}\n"
        message += f" - Stop: {idea['stop']}\n"
        message += f" - Target: {idea['target']}\n"
    return message

def send_post_open_ideas():
    data = generate_post_open_ideas()
    message = format_trade_ideas(data)
    bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)

if __name__ == "__main__":
    send_post_open_ideas()
