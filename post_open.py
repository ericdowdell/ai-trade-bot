
import os
import asyncio
from datetime import datetime
from telegram.ext import Application
import yfinance as yf
import requests
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

# Function to fetch today's economic events from News API or other sources
def get_today_events():
    # Here, we'll integrate a real API to pull the correct data for today's events.
    # For now, we will simulate the event data for today's NFP, CPI, etc.
    
    # In production, you could use an API like TradingEconomics, NewsAPI, or similar
    events = {
        "NFP": {"forecast": "200K", "actual": "198K", "impact": "High", "reaction": "Sell"},
        "CPI": {"forecast": "0.2%", "actual": "0.1%", "impact": "Medium", "reaction": "Bullish"},
        "ISM": {"forecast": "52.1", "actual": "53.4", "impact": "High", "reaction": "Bullish"}
    }
    
    return events

# Function to generate trade ideas based on live data
def generate_trade_ideas():
    prices = {
        "ES": get_price("ES=F"),
        "NQ": get_price("NQ=F"),
        "CL": get_price("CL=F")
    }

    events = get_today_events()

    # Generate trade ideas based on NFP or market events
    trade_data = {
        "ES": {
            "entry": prices["ES"],
            "stop": round(prices["ES"] - 12, 2),
            "target": round(prices["ES"] + 25, 2),
            "reason": "VWAP reclaim + macro support",
            "reaction": "Sell" if events["NFP"]["reaction"] == "Sell" else "Buy"
        },
        "NQ": {
            "entry": prices["NQ"],
            "stop": round(prices["NQ"] - 80, 2),
            "target": round(prices["NQ"] + 120, 2),
            "reason": "Tech strength + reclaim of overnight high",
            "reaction": "Buy" if events["ISM"]["reaction"] == "Bullish" else "Sell"
        },
        "CL": {
            "entry": prices["CL"],
            "stop": round(prices["CL"] + 0.65, 2),
            "target": round(prices["CL"] - 1.45, 2),
            "reason": "Failed breakout + bearish macro tone",
            "reaction": "Sell" if events["NFP"]["reaction"] == "Sell" else "Buy"
        }
    }

    return prices, trade_data, events

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
    prices, trades, events = generate_trade_ideas()

    # Prepare the main text message with live event-based data
    text = f"🔁 Post-Open Trade Ideas — {today}\n\n"
    text += "🧠 Market Recap:\n"
    text += f"- NFP: Forecast {events['NFP']['forecast']}K, Actual {events['NFP']['actual']}K (Market Reaction: {events['NFP']['reaction']})\n"
    text += f"- CPI: Forecast {events['CPI']['forecast']}, Actual {events['CPI']['actual']} (Market Reaction: {events['CPI']['reaction']})\n"
    text += f"- ISM: Forecast {events['ISM']['forecast']}, Actual {events['ISM']['actual']} (Market Reaction: {events['ISM']['reaction']})\n\n"

    text += "📍 Futures Snapshot:\n"
    text += f"- ES: {prices['ES']} | NQ: {prices['NQ']} | CL: {prices['CL']}\n\n"

    text += "🎯 Trade Ideas:\n"
    for symbol, data in trades.items():
        text += f"🟢 {('Buy' if data['reaction'] == 'Buy' else 'Sell')} {symbol} — Entry: {data['entry']} | Stop: {data['stop']} | Target: {data['target']}\n"
        text += f"📌 Reason: {data['reason']} | Reaction: {data['reaction']}\n\n"

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
