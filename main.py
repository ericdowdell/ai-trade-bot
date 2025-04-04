
import os
import json
import asyncio
import logging
from datetime import datetime
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def load_trade_ideas():
    with open("trade_ideas.json", "r") as f:
        return json.load(f)

def format_message(trade_data):
    today = datetime.now().strftime("%B %d")
    message = f"📊 Trade Ideas — {today}\n"
    for symbol, idea in trade_data.items():
        message += f"\n{idea['bias']} {symbol}\n"
        message += f" - Reason: {idea['reason']}\n"
        message += f" - Entry: {idea['entry']}\n"
        message += f" - Stop: {idea['stop']}\n"
        message += f" - Target: {idea['target']}\n"
    return message

async def send_daily_trade_ideas():
    try:
        data = load_trade_ideas()
        message = format_message(data)
        await bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
    except Exception as e:
        logging.error(f"Error sending message: {e}")

if __name__ == "__main__":
    asyncio.run(send_daily_trade_ideas())
