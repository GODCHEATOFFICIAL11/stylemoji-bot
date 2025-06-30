from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from utils.sticker import create_new_pack, add_sticker
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 1209978813
CHANNELS = [
    {"id": -1001857302142, "link": "https://t.me/+ZUXtxXBzR_VkMjU1"},
    {"id": None, "link": "https://t.me/+XvJd4DeTig5hYzE9"}
]

HELP_TEXT = """🤖 *How to use StyleMojiBot*

Welcome to your personal sticker bot! Here's what you can do:

🆕 /new – Create a new sticker pack  
➕ /add – Send a photo to convert it into a sticker  
✅ /done – Finalize your pack  
📦 /list – View your current session pack  
🎨 /moji – Turn an emoji into a style sticker  
📚 /help – Show this help message

⚠ You must join Channel 1 to use this bot."""

async def check_membership(user_id, bot):
    ch = CHANNELS[0]
    try:
        member = await bot.get_chat_member(chat_id=ch["id"], user_id=user_id)
        if member.status in ['left', 'kicked']:
            return False
    except:
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        msg = f"🚀 New User Started the Bot\n\n👤 Name: {user.full_name}\n🆔 User ID: {user.id}\n🔗 Username: @{user.username}" if user.username else f"🚀 New User Started the Bot\n\n👤 Name: {user.full_name}\n🆔 User ID: {user.id}\n🔗 Username: No username"
        await context.bot.send_message(chat_id=OWNER_ID, text=msg)
    except:
        pass

    if not await check_membership(user.id, context.bot):
        buttons = [
            [InlineKeyboardButton("📢 Join Channel 1", url=CHANNELS[0]["link"])],
            [InlineKeyboardButton("📢 Join Channel 2 (optional)", url=CHANNELS[1]["link"])],
            [InlineKeyboardButton("✅ I've Joined", callback_data="verify_join")]
        ]
        await update.message.reply_text("🔐 To use this bot, please join the required channel:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    keyboard = [["💖 Create love name status"], ["📦 List of my packs"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("✅ You're in! Choose an option:", reply_markup=markup)

async def verify_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await check_membership(query.from_user.id, context.bot):
        await query.edit_message_text("❌ You're still not a member of the required channel.")
        return

    keyboard = [["💖 Create love name status"], ["📦 List of my packs"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await query.edit_message_text("✅ You're in! Choose an option:")
    await context.bot.send_message(chat_id=query.message.chat_id, text="Choose an option:", reply_markup=markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")

async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send name for your new sticker pack:")
    context.user_data["creating_pack"] = True

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("creating_pack"):
        name = update.message.text
        await create_new_pack(update, context, name)
        context.user_data["creating_pack"] = False

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify_join, pattern="verify_join"))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("new", new))
app.add_handler(MessageHandler(filters.PHOTO, add_sticker))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.run_polling()
