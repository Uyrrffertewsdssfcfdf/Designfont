import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

logging.basicConfig(level=logging.INFO)

# ===== تنظیمات =====
BOT_TOKEN = "6869838687:AAGdJTM-tv3tcvEYJlFjUNPYz4MS83HW86w"
CHANNEL_ID = "@designfont6"
ADMIN_ID = 1836165249  # آیدی عددی خودت رو اینجا بذار

# ===== فایل‌های فونت =====
FONTS = {
    "arzhan": {"name": "ارژن | Arzhan", "file_id": ""},
    "atabay": {"name": "آتابای | Atabay", "file_id": ""},
    "azhdar": {"name": "اژدر | Azhdar", "file_id": ""},
    "ebtekar": {"name": "ابتکار | Ebtekar", "file_id": ""},
    "family_iran": {"name": "خانواده فونت ایران | Family Font IRAN", "file_id": ""},
    "faramrzian": {"name": "فرامرزیان | Faramrzian", "file_id": ""},
    "gohar": {"name": "گوهر | Gohar", "file_id": ""},
    "hamideh": {"name": "حمیده ساعیان | Hamideh Saeian", "file_id": ""},
    "hilda": {"name": "هیلدا | Hilda", "file_id": ""},
    "hoda": {"name": "هدی | Hoda", "file_id": ""},
    "iran_dorandis": {"name": "ایران درندیس | IRAN Dorandis", "file_id": ""},
    "iran_kharazmi": {"name": "ایران خوارزمی | IRAN Kharazmi", "file_id": ""},
    "iran_marker": {"name": "ایران مارکر | IRAN Marker", "file_id": ""},
    "iran_rounded": {"name": "ایران گرد | IRAN Rounded", "file_id": ""},
    "iran_dastnevis": {"name": "ایران سنس دستنویس | IRAN Sans DastNevis", "file_id": ""},
    "iran_sharp": {"name": "ایران شارپ | IRAN Sharp", "file_id": ""},
    "kamva": {"name": "کاموا | Kamva", "file_id": ""},
    "katibeh": {"name": "کتیبه | Katibeh", "file_id": ""},
    "mahboubeh": {"name": "محبوبه مهرآور | Mahboubeh Mehravar", "file_id": ""},
    "roosta": {"name": "روستا | Roosta", "file_id": ""},
    "tahamtan": {"name": "تهمتن | Tahamtan", "file_id": ""},
    "titr_grafiti": {"name": "تیتر گرافیتی | Titr Graphiti", "file_id": ""},
    "titr_zebr": {"name": "تیتر زبر | Titr Zebr", "file_id": ""},
}

async def is_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramError:
        return False

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/designfont6")],
        [InlineKeyboardButton("✅ عضو شدم، بررسی کن", callback_data="check_membership")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    font_key = args[0] if args else None

    if font_key and font_key in FONTS:
        if not await is_member(user_id, context):
            context.user_data["pending_font"] = font_key
            await update.message.reply_text(
                "⚠️ برای دریافت فونت باید عضو کانال ما باشی!\n\n"
                "👇 اول عضو شو بعد دکمه «عضو شدم» رو بزن:",
                reply_markup=join_keyboard()
            )
            return
        await send_font_file(update.message, font_key, context)
    else:
        if not await is_member(user_id, context):
            await update.message.reply_text(
                "سلام! 👋\n\n"
                "⚠️ برای استفاده از ربات باید عضو کانال ما باشی:",
                reply_markup=join_keyboard()
            )
            return
        await show_menu(update.message)

async def show_menu(message):
    keyboard = []
    font_list = list(FONTS.items())
    for i in range(0, len(font_list), 2):
        row = []
        row.append(InlineKeyboardButton(
            f"🔤 {font_list[i][1]['name'].split('|')[0].strip()}",
            callback_data=f"font_{font_list[i][0]}"
        ))
        if i + 1 < len(font_list):
            row.append(InlineKeyboardButton(
                f"🔤 {font_list[i+1][1]['name'].split('|')[0].strip()}",
                callback_data=f"font_{font_list[i+1][0]}"
            ))
        keyboard.append(row)

    await message.reply_text(
        "🎨 *دیزاین فونت*\n\nفونت مورد نظرت رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def send_font_file(message, font_key, context):
    font = FONTS.get(font_key)
    if not font:
        await message.reply_text("❌ فونت پیدا نشد!")
        return
    if not font["file_id"]:
        await message.reply_text(
            f"⏳ فونت *{font['name']}* هنوز آپلود نشده!\nبه زودی اضافه میشه 🙏",
            parse_mode="Markdown"
        )
        return
    await message.reply_text(f"⏳ در حال ارسال...", parse_mode="Markdown")
    await context.bot.send_document(
        chat_id=message.chat_id,
        document=font["file_id"],
        caption=f"🔤 *{font['name']}*\n\n📢 کانال: @designfont6",
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check_membership":
        if await is_member(user_id, context):
            pending = context.user_data.get("pending_font")
            if pending:
                context.user_data.pop("pending_font")
                await send_font_file(query.message, pending, context)
            else:
                await show_menu(query.message)
        else:
            await query.message.reply_text(
                "❌ هنوز عضو کانال نشدی!\nاول عضو بشو بعد دوباره بزن ✅",
                reply_markup=join_keyboard()
            )

    elif query.data.startswith("font_"):
        font_key = query.data[5:]
        if not await is_member(user_id, context):
            context.user_data["pending_font"] = font_key
            await query.message.reply_text(
                "⚠️ برای دریافت فونت باید عضو کانال باشی!",
                reply_markup=join_keyboard()
            )
            return
        await send_font_file(query.message, font_key, context)

async def upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return
    if update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
        await update.message.reply_text(
            f"✅ فایل دریافت شد!\n\n"
            f"📁 نام: `{file_name}`\n"
            f"🔑 File ID:\n`{file_id}`",
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, upload_handler))
    print("✅ ربات شروع به کار کرد!")
    app.run_polling()

if __name__ == "__main__":
    main()
