import discord
import requests
import asyncio
import os

TOKEN = os.getenv("TOKEN") or "PUT_YOUR_BOT_TOKEN_HERE"
CHANNEL_ID = int(os.getenv("CHANNEL_ID") or 123456789012345678)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def get_stock():
    url = "https://blox-fruits-stock.vercel.app/api/stock"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            fruits = data.get('stock', [])
            stock_text = "📦 **Blox Fruits Dealer Stock (Normal):**\n\n"
            for fruit in fruits:
                name = fruit.get('name')
                price = fruit.get('price')
                stock_text += f"🍇 **{name}** — 💸 `{price}` Beli\n"
            return stock_text
        else:
            return "🚫 Could not fetch fruit stock (API error)."
    except Exception as e:
        return f"❌ Error fetching stock: {e}"

@client.event
async def on_ready():
    print(f'🟢 Bot is online as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    while True:
        stock_msg = await get_stock()
        await channel.send(stock_msg)
        await asyncio.sleep(4 * 60 * 60)  # Repeat every 4 hours

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!stock'):
        stock_msg = await get_stock()
        await message.channel.send(stock_msg)

    if message.content.lower().startswith('!help'):
        help_text = (
            "📘 **Blox Fruits Stock Bot Commands:**\n"
            "📍 `!stock` – Show current dealer stock\n"
            "🆘 `!help` – Show this help message"
        )
        await message.channel.send(help_text)

client.run(TOKEN)
