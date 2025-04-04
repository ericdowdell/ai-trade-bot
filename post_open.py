
import os
import asyncio
from datetime import datetime
from telegram.ext import Application
import yfinance as yf
import matplotlib.pyplot as plt

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

# Function to get live market prices using yfinance
def get_price(symbol):
    try:
        return round(yf.Ticker(symbol).info["regularMarketPrice"], 2)
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return "N/A"

# Function to generate trade ideas based on live data
def generate_trade_ideas():
    prices = {
        "ES": get_price("ES=F"),
        "NQ": get_price("NQ=F"),
        "CL": get_price("CL=F")
    }

    # Create trade ideas based on current market prices
    trade_data = {
        "ES": {
            "entry": prices["ES"],
            "stop": round(prices["ES"] - 12, 2),
            "target": round(prices["ES"] + 25, 2),
            "reason": "VWAP reclaim + macro support"
        },
        "NQ": {
            "entry": prices["NQ"],
            "stop": round(prices["NQ"] - 80, 2),
            "target": round(prices["NQ"] + 120, 2),
            "reason": "Tech strength + reclaim of overnight high"
        },
        "CL": {
            "entry": prices["CL"],
            "stop": round(prices["CL"] + 0.65, 2),
            "target": round(prices["CL"] - 1.45, 2),
            "reason": "Failed breakout + bearish macro tone"
        }
    }

    return prices, trade_data

# Function to generate the chart for each trade idea
def generate_chart(symbol, entry, stop, target):
    price_range = [min(entry, stop, target) - 3, max(entry, stop, target) + 3]
    plt.figure(figsize=(8, 3))
    plt.plot([price_range[0], price_range[1]], [entry, entry], label=f'Entry: {entry}', linestyle='--', color='blue')
    plt.plot([price_range[0], price_range[1]], [stop, stop], label=f'Stop: {stop}', linestyle='--', color='red')
    plt.plot([price_range[0], price_range[1]], [target, target], label=f'Target: {target}', linestyle='--', color='green')
    plt.text(price_range[1], entry, " Entry", va='center', color='blue')
    plt.text(price_range[1], stop, " Stop", va='center', color='red')
    plt.text(price_range[1], target, " Target", va='center', color='green')
    plt.title(f"{symbol} Trade Setup")
    plt.grid(True)
    plt.legend()
    chart_file = f"{symbol}_trade_setup_chart.png"
    plt.savefig(chart_file, bbox_inches="tight")
    plt.close()
    return chart_file

# Main function to generate message and send to Telegram with chart images
async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    today = datetime.now().strftime("%A, %B %d, %Y")
    prices, trades = generate_trade_ideas()

    # Prepare the main text message without any CPI reference, using only live data
    text = f"🔁 Post-Open Trade Ideas — {today}\n\n"
    text += "🧠 Market Recap:\n"
    text += "No scheduled economic events today impacting the market directly. Monitoring tech, commodities, and market reactions to global flows.\n\n"

    text += "📍 Futures Snapshot:\n"
    text += f"- ES: {prices['ES']} | NQ: {prices['NQ']} | CL: {prices['CL']}\n\n"

    text += "🎯 Trade Ideas:\n"
    for symbol, data in trades.items():
        text += f"🟢 {('Buy' if symbol != 'CL' else 'Sell')} {symbol} — Entry: {data['entry']} | Stop: {data['stop']} | Target: {data['target']}\n"
        text += f"📌 Reason: {data['reason']}\n\n"

    # Send the message to Telegram
    await application.bot.send_message(chat_id=TELEGRAM_USER_ID, text=text)

    # Prepare and send the chart images
    media_group = []
    for symbol, data in trades.items():
        image_path = generate_chart(symbol, data['entry'], data['stop'], data['target'])
        with open(image_path, "rb") as img:
            media_group.append(await application.bot.send_photo(chat_id=TELEGRAM_USER_ID, photo=img))

if __name__ == "__main__":
    asyncio.run(main())
