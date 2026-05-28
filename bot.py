import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن ربات خودت رو اینجا بذار
BOT_TOKEN = "6869838687:AAGdJTM-tv3tcvEYJlFjUNPYz4MS83HW86w"

# مسیر فایل فونت
FONT_FILE = "font.zip"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📥 دریافت فونت", callback_data="get_font")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "سلام! 👋\nبرای دریافت فونت دکمه زیر رو بزن:",
        reply_markup=reply_markup
    )

async def send_font(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("⏳ در حال ارسال فایل...")
    with open(FONT_FILE, "rb") as f:
        await query.message.reply_document(document=f, filename="font.zip")

from telegram.ext import CallbackQueryHandler

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(send_font, pattern="get_font"))
    print("ربات شروع به کار کرد...")
    app.run_polling()
