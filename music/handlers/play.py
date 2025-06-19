from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, AudioPiped
from youtube_dl import YoutubeDL
import os

# Pyrogram client and PyTgCalls from bot.py
from config import OWNER_ID
from bot import app, pytgcalls

# Song download settings
YDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'quiet': True
}

def yt_search(query):
    with YoutubeDL(YDL_OPTS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            return info['webpage_url']
        except Exception as e:
            return None

def download_song(url):
    with YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def is_admin(member):
    return member.status in ("administrator", "creator")

@app.on_message(filters.command("play") & filters.group)
async def play_song(_, message: Message):
    user = message.from_user
    chat_id = message.chat.id

    # Admin check
    member = await app.get_chat_member(chat_id, user.id)
    if not is_admin(member) and user.id != OWNER_ID:
        return await message.reply("❌ Sirf admin hi music chala sakta hai.")

    query = " ".join(message.command[1:]) if len(message.command) > 1 else None

    if not query and message.reply_to_message and message.reply_to_message.audio:
        file_path = await message.reply_to_message.download()
    elif query:
        url = yt_search(query)
        if not url:
            return await message.reply("❌ Song nahi mila YouTube pe.")
        file_path = download_song(url)
    else:
        return await message.reply("⚠️ Usage: `/play song name` ya kisi audio ko reply karo.")

    await pytgcalls.join_group_call(
        chat_id,
        InputStream(
            AudioPiped(file_path)
        ),
        stream_type="local_stream"
    )

    await message.reply_text(
        f"🎶 Playing now: **{os.path.basename(file_path)}**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⏹ Stop", callback_data="stop_music")]
        ])
    )

@app.on_callback_query(filters.regex("stop_music"))
async def stop_music(_, callback_query):
    chat_id = callback_query.message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await callback_query.message.edit("🛑 Music stopped.")
