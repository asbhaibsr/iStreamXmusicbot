from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, SESSION_STRING, OWNER_ID
from pytgcalls import GroupCallFactory
from ping_server import keep_alive
from utils.ai_reply import generate_ai_reply
from utils.music_stream import play_music, stop_music
import asyncio

# Keep alive (Koyeb uptime)
keep_alive()

# Pyrogram session client
app = Client(
    name="music-ai-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# VC streaming client
pytgcalls = GroupCallFactory(app).get_group_call()


# /start command
@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    await message.reply_text(
        "**💫 𝙷𝚒 𝙷𝚞 𝙼𝚞𝚜𝚒𝚌 + 𝙰𝙸 𝙱𝚘𝚝 𝚋𝚢 @asbhaibsr**\n\n"
        "🎵 Add me to group & use /play\n"
        "💌 Chat with me for AI replies",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add To Group", url="https://t.me/asmusicbotandaichat?startgroup=true")],
            [InlineKeyboardButton("📢 Update Channel", url="https://t.me/asbhai_bsr")],
            [InlineKeyboardButton("🎬 Movie Group", url="https://t.me/iStreamX")]
        ])
    )


# Group AI reply
@app.on_message(filters.group & ~filters.command("play") & ~filters.command("stop") & ~filters.bot)
async def ai_chat(_, message: Message):
    text = message.text
    if not text:
        return
    await message.reply_chat_action("typing")
    reply = await generate_ai_reply(message.from_user.id, text)
    if reply and reply.strip() != "...":
        await message.reply_text(reply)


# Music play command (admin only)
@app.on_message(filters.command("play") & filters.group)
async def play(_, message: Message):
    await play_music(app, pytgcalls, message)


# Music stop
@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message: Message):
    await stop_music(pytgcalls, message)


# Run bot
async def main():
    await app.start()
    await pytgcalls.start()
    print("Bot is running...")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
