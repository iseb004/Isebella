from flask import Flask
import threading
import os
from pyrogram import Client, filters

# Read secrets from environment variables
API_ID = int(os.environ.get("API_ID", "123456"))        # default just in case
API_HASH = os.environ.get("API_HASH", "default_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "default_bot_token")

# Initialize Pyrogram bot client
bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Render will pass $PORT
    app.run(host='0.0.0.0', port=port)

# Define a command handler
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("✅ Hello! Your bot is working!")

if __name__ == "__main__":
    # Start Flask server in background
    threading.Thread(target=run_flask).start()
    # Start the bot
    bot.run()
