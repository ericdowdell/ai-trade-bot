
import os
import json
import asyncio
import logging
from datetime import datetime
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# STEP 1: Generate new trade ideas (live-style)
def generate_trade_ideas():
    ideas = {
        "ES": {
            "bias": "🟢 Buy",
            "reason": "CPI slowed + ECB rate cut supports risk-on sentiment",
            "entry": "5275.00",
            "stop": "5258.00",
            "target": "5315.00"
        },
        "NQ": {
            "bias": "🟢 Buy",
            "reason": "Tech leading on cooling inflation expectations",
            "entry": "18320.00",
            "stop": "18200.00",
            "target": "18520.00"
        },
        "YM": {
            "bias": "⚠️ Neutral",
            "reason": "Dow remains directionless amid sector rotation",
            "entry": "—",
            "stop": "—",
            "target": "—"
        },
        "GC": {
            "bias": "🟢 Buy",
            "reason": "Lower real yields + geopolitical risk support safe havens",
            "entry": "2312.00",
            "stop": "2298.00",
            "target": "2345.00"
        },
        "CL": {
            "bias": "🔴 Sell",
            "reason": "EIA shows inventory build; demand outlook weak",
            "entry": "84.70",
            "stop": "85.60",
            "target": "82.90"
        }
    }
    with open("trade_ideas.json", "w") as f:
        json.dump(ideas, f, indent=4)
    return ideas

# STEP 2: Format the message
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

# STEP 3: Send to Telegram
async def send_trade_ideas():
    try:
        ideas = generate_trade_ideas()
        message = format_message(ideas)
        await bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
    except Exception as e:
        logging.error(f"Error sending trade ideas: {e}")

if __name__ == "__main__":
    asyncio.run(send_trade_ideas())
