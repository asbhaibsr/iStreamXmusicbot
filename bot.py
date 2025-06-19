import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, SESSION_STRING
from music.handlers.play import music_commands
from ai import generate_ai_reply
from ping_server import keep_alive

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
pytgcalls = PyTgCalls(app)

ai_enabled = {}

@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    await message.reply_text(
        "**👋 Hey jaanu!**\n\n"
        "Main ek stylish girl bot hoon 😘\n"
        "🧠 AI chat aur 🎧 music dono handle karti hoon!\n\n"
        "Mujhe group me le jao aur maze lo 😍",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await app.get_me()).username}?startgroup=true")],
            [InlineKeyboardButton("🎬 Movie Group", url="https://t.me/iStreamX")],
            [InlineKeyboardButton("📢 Update Channel", url="https://t.me/asbhai_bsr")]
        ])
    )

@app.on_message(filters.command("ai") & filters.group)
async def toggle_ai(_, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply("Use: /ai on ya /ai off")
    if message.command[1] == "on":
        ai_enabled[chat_id] = True
        await message.reply("✅ AI Enabled.")
    elif message.command[1] == "off":
        ai_enabled[chat_id] = False
        await message.reply("❌ AI Disabled.")

@app.on_message(filters.text & filters.group & ~filters.command(["play", "skip", "stop"]))
async def ai_reply(_, message: Message):
    if ai_enabled.get(message.chat.id):
        reply = await generate_ai_reply(message.from_user.id, message.text)
        await message.reply_text(reply)

async def main():
    keep_alive()
    await app.start()
    await pytgcalls.start()
    print("🤖 Bot chalu ho gaya!")
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
