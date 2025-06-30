from PIL import Image
import io

async def create_new_pack(update, context, name):
    user = update.effective_user
    pack_name = f"{name}_by_StyleMojiBot"
    context.user_data["pack_name"] = pack_name
    await update.message.reply_text(f"✅ Sticker pack created: {pack_name}\nNow send a photo to add as sticker.")

async def add_sticker(update, context):
    user = update.effective_user
    pack_name = context.user_data.get("pack_name", "default_by_StyleMojiBot")
    if not update.message.photo:
        await update.message.reply_text("❌ Please send a photo to add as sticker.")
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    bio = io.BytesIO()
    await file.download_to_memory(out=bio)
    bio.seek(0)
    img = Image.open(bio).convert("RGBA")
    img = img.resize((512, 512))
    output = io.BytesIO()
    output.name = "sticker.webp"
    img.save(output, "WEBP")
    output.seek(0)

    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=output)
    await update.message.reply_text(f"🖼️ Sticker added to {pack_name}")
