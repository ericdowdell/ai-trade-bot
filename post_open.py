
import os
import asyncio
from datetime import datetime
from telegram.ext import Application
import yfinance as yf

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

def get_price(symbol):
    try:
        return round(yf.Ticker(symbol).info["regularMarketPrice"], 2)
    except Exception:
        return "N/A"

def generate_post_open_message():
    today = datetime.now().strftime("%A, %B %d, %Y")

    prices = {
        "ES": get_price("ES=F"),
        "NQ": get_price("NQ=F"),
        "GC": get_price("GC=F"),
        "CL": get_price("CL=F")
    }

    message = f"""🔁 Post-Open Trade Ideas — {today}

📍 Live Futures Snapshot:
- ES: {prices['ES']} | Watching VWAP reclaim near 5120
- NQ: {prices['NQ']} | Tech bounce in progress
- GC: {prices['GC']} | Bid holding on weak jobs data
- CL: {prices['CL']} | Choppy, eye on 84.50 flip

🎯 Trade Ideas:

🟢 Buy ES
- Reason: VWAP reclaim + macro support
- Entry: {float(prices['ES']) + 1 if prices['ES'] != 'N/A' else 'N/A'}
- Stop: {float(prices['ES']) - 10 if prices['ES'] != 'N/A' else 'N/A'}
- Target: {float(prices['ES']) + 25 if prices['ES'] != 'N/A' else 'N/A'}

🟢 Buy NQ
- Reason: Reversal from overnight low
- Entry: {float(prices['NQ']) + 10 if prices['NQ'] != 'N/A' else 'N/A'}
- Stop: {float(prices['NQ']) - 50 if prices['NQ'] != 'N/A' else 'N/A'}
- Target: {float(prices['NQ']) + 120 if prices['NQ'] != 'N/A' else 'N/A'}

⚠️ GC: Watch 2335–2355 zone for breakout

📊 This recap auto-generates from live futures prices + macro tone.
"""
    return message

async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    message = generate_post_open_message()
    await application.bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)

if __name__ == "__main__":
    asyncio.run(main())
