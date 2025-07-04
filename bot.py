
from pyrogram import Client, filters
from config import Config
import os
import asyncio

bot = Client(
    "rename_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Store user file context
user_files = {}

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        "**👋 Welcome!**\n\n"
        "• Send me a file to rename.\n"
        "• Reply to a photo with /thumbnail to set thumbnail.\n"
        "• I support doing multiple renames at once!"
    )

@bot.on_message(filters.command("thumbnail") & filters.private)
async def set_thumbnail(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        thumb_path = f"{message.from_user.id}.jpg"
        await message.reply_to_message.download(file_name=thumb_path)
        await message.reply_text("✅ Thumbnail saved!")
    else:
        await message.reply_text("❗ Reply to a photo with /thumbnail to set it.")

@bot.on_message((filters.document | filters.video | filters.audio) & filters.private)
async def ask_new_name(client, message):
    user_files[message.from_user.id] = message
    await message.reply_text("✏️ Send me the new filename (without extension).")

@bot.on_message(filters.text & filters.private)
async def process_rename(client, message):
    user_id = message.from_user.id
    if user_id in user_files:
        old_msg = user_files.pop(user_id)
        media = old_msg.document or old_msg.video or old_msg.audio
        new_filename = message.text + "." + media.file_name.split(".")[-1]
        thumb_path = f"{user_id}.jpg"
        temp_path = f"{user_id}_{new_filename}"

        await message.reply_text("⏳ Downloading & uploading... please wait.")

        async def rename_task():
            try:
                # Download locally
                await old_msg.download(file_name=temp_path)

                # Upload to storage channel
                sent_msg = await client.send_document(
                    chat_id=Config.CHANNEL_ID,
                    document=temp_path,
                    file_name=new_filename,
                    caption=f"📦 Renamed: {new_filename}",
                    thumb=thumb_path if os.path.exists(thumb_path) else None
                )

                # Delete local temp file
                os.remove(temp_path)

                # Create link
                channel_id_str = str(Config.CHANNEL_ID)
                if channel_id_str.startswith("-100"):
                    channel_id_str = channel_id_str[4:]
                file_link = f"https://t.me/c/{channel_id_str}/{sent_msg.id}"

                await message.reply_text(f"✅ Done! [Download here]({file_link})", disable_web_page_preview=True)
            except Exception as e:
                await message.reply_text(f"❌ Failed: {e}")

        # Run as task to support multiple concurrent uploads
        asyncio.create_task(rename_task())
    else:
        await message.reply_text("❗ Send me a file first.")

print("✅ Bot started successfully!")
bot.run()
