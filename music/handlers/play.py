from pytgcalls.types.input_stream import AudioPiped
from pytgcalls import StreamType
from pytgcalls.types.input_stream.quality import HighQualityAudio

from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from config import SESSION_STRING, API_ID, API_HASH
from pyrogram import Client
import asyncio
import yt_dlp

# Session for streaming (internal use)
user = Client("user", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
pytgcalls = GroupCallFactory(user).get_group_call()


async def play_music(app, pytgcalls, message: Message):
    if not message.reply_to_message or not message.reply_to_message.audio:
        return await message.reply_text("🎵 Reply to an audio file to stream!")

    audio = message.reply_to_message.audio
    file_path = await app.download_media(audio)

    await pytgcalls.join_group_call(
        message.chat.id,
        AudioPiped(file_path, HighQualityAudio()),
        stream_type=StreamType().pulse_stream,
    )
    await message.reply_text(f"🎶 Now Playing: {audio.title or 'Audio'}")


async def stop_music(pytgcalls, message: Message):
    await pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("⛔ Music stopped.")
