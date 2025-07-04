from pyrogram import Client, filters
from flask import Flask
import threading
import os

# Read from environment variables
API_ID = int(os.environ.get("API_ID", "123456"))           # replace default with your real API_ID
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

# Create Pyrogram bot client
bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Example command: /start
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! ✅ Bot is running.")

if __name__ == "__main__":
    # Start Flask server in background
    threading.Thread(target=run_flask).start()
    # Start the bot
    bot.run()
