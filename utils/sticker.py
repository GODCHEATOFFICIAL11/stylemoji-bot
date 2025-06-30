from io import BytesIO
from pyrogram import Client
from pyrogram.types import Message


async def create_new_pack(bot: Client, message: Message, emoji: str, png_sticker: BytesIO, pack_name: str, pack_title: str):
    try:
        response = await bot.create_new_sticker_set(
            user_id=message.from_user.id,
            name=pack_name,
            title=pack_title,
            png_sticker=png_sticker,
            emojis=emoji
        )
        return True
    except Exception as e:
        await message.reply_text(f"Error creating pack:\n{e}")
        return False


async def add_sticker(bot: Client, message: Message, emoji: str, png_sticker: BytesIO, pack_name: str):
    try:
        response = await bot.add_sticker_to_set(
            user_id=message.from_user.id,
            name=pack_name,
            png_sticker=png_sticker,
            emojis=emoji
        )
        return True
    except Exception as e:
        await message.reply_text(f"Error adding sticker:\n{e}")
        return False
      
