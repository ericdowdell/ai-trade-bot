
import os
import asyncio
from datetime import datetime
from telegram.ext import Application

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

def get_calendar_summary():
    try:
        with open("calendar_summary.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "📅 No economic events found for today."

def generate_pre_market_message():
    today = datetime.now().strftime("%B %d, %Y")
    macro_summary = f"""📊 Pre-Market Overview — {today}

🌍 Global Macro Highlights:
- Asia mixed, Europe flat ahead of US data
- Traders eye Fed reaction to jobs data

{get_calendar_summary()}

🎯 Pre-Market Bias:
🟢 GC — Favor long above 2305
⚠️ ES — Wait for confirmation post open
🔴 CL — Weak below 84.50
"""
    return macro_summary

async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    message = generate_pre_market_message()
    await application.bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)

if __name__ == "__main__":
    asyncio.run(main())
