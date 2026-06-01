import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8832863407:AAGsKKeM8ZwYvdaCyh4iTIq-kowZ4WMDIT0"
CHANNEL_ID = "@designfont6"
ADMIN_ID = 1836165249  # آیدی عددی خودت

FONTS = {
    "ahang": {"name": "آهنگ | Ahang", "file_id": "BQACAgQAAxkBAAN4ahzE73IEOwyjZgX-ZsWXiYw5DXcAAukgAAI8zehQRXQPLrqoG8I7BA"},
    "arzhan": {"name": "ارژن | Arzhan", "file_id": "BQACAgQAAxkBAAN5ahzE70X2rw004Z5V-4UBxp-4KDsAAuogAAI8zehQcG08T9Paeck7BA"},
    "atabay": {"name": "آتابای | Atabay", "file_id": "BQACAgQAAxkBAAN6ahzE779CBs5YqUxqhbo3g-BE2s0AAusgAAI8zehQkUX12gGmbe47BA"},
    "aviny": {"name": "آوینی | Aviny", "file_id": "BQACAgQAAxkBAAN7ahzE7ye1ZbyAaTFPwQABQ6sI2-W4AALsIAACPM3oUK3muQsKQQvJOwQ"},
    "azhdar": {"name": "اژدر | Azhdar", "file_id": "BQACAgQAAxkBAAN8ahzE73GdcSa5vsIG5xrMdZ2RswEAAu0gAAI8zehQZG-MZ7C_cak7BA"},
    "damavand": {"name": "دماوند | Damavand", "file_id": "BQACAgQAAxkBAAN9ahzE78_pieL5AAGzjcrHIDmBX1Z6AALuIAACPM3oUA5J5GDaUux_OwQ"},
    "ebtekar": {"name": "ابتکار | Ebtekar", "file_id": "BQACAgQAAxkBAAN-ahzE76pzWS20_jNvujQe-w5GGo0AAu8gAAI8zehQ9n8izJngq0A7BA"},
    "emkan": {"name": "امکان | Emkan", "file_id": "BQACAgQAAxkBAAN_ahzE7ydqek97CPmF6Z84ID19bHgAAvAgAAI8zehQzTJOPlhlZUc7BA"},
    "family_iran": {"name": "خانواده فونت ایران | Family Font IRAN", "file_id": "BQACAgQAAxkBAAOAahzE75NdOOVxdldLQQLwtW-JUw0AAvEgAAI8zehQsFVTbNB_hcU7BA"},
    "faramrzian": {"name": "فرامرزیان | Faramrzian", "file_id": "BQACAgQAAxkBAAOBahzE7yRoUyxzyii0-YSPvDbW6PkAAvIgAAI8zehQN8NAKxGANv07BA"},
    "gohar": {"name": "گوهر | Gohar", "file_id": "BQACAgQAAxkBAAOMahzFC6tK1Mz_8Bmgq9f9T7JtsF4AAvMgAAI8zehQIxWRfTpVg_E7BA"},
    "golpayegani": {"name": "گلپایگانی | Golpayegani", "file_id": "BQACAgQAAxkBAAONahzFCz9E3fqqqGSnlWGDx5tElUMAAvQgAAI8zehQX7ePw3Nikm87BA"},
    "hamideh": {"name": "حمیده ساعیان | Hamideh Saeian", "file_id": "BQACAgQAAxkBAAOOahzFCwrxv6l-m8t260S438yTlqMAAvUgAAI8zehQTA16DgrNYqU7BA"},
    "hamta": {"name": "همتا | Hamta", "file_id": "BQACAgQAAxkBAAOPahzFC2ERf5jVFJyZBUUmjzcbTRwAAvYgAAI8zehQvS-JJ6z_B9A7BA"},
    "hilda": {"name": "هیلدا | Hilda", "file_id": "BQACAgQAAxkBAAOQahzFCzLnYCuNUkCeI6cXOtnsZmsAAvcgAAI8zehQuBRBPlecAAEzOwQ"},
    "hoda": {"name": "هدی | Hoda", "file_id": "BQACAgQAAxkBAAORahzFC9gzQy9wpd9DPwIp7S8Nl3wAAvggAAI8zehQgtgcz1JAIdU7BA"},
    "iran_dorandis": {"name": "ایران درندیس | IRAN Dorandis", "file_id": "BQACAgQAAxkBAAOSahzFC1D-1whbpZJ5pRvXrep88mkAAvkgAAI8zehQtKJG3yElJz47BA"},
    "iran_kharazmi": {"name": "ایران خوارزمی | IRAN Kharazmi", "file_id": "BQACAgQAAxkBAAOTahzFC_sz13wxJPhEULn3jy26rhMAAvogAAI8zehQWHZRos8HdsI7BA"},
    "iran_marker": {"name": "ایران مارکر | IRAN Marker", "file_id": "BQACAgQAAxkBAAOUahzFC-o2umDm1yaDPWydd_IsR_wAAvsgAAI8zehQGLm9_W3tSjs7BA"},
    "iran_rounded": {"name": "ایران گرد | IRAN Rounded", "file_id": "BQACAgQAAxkBAAOVahzFC0BW0yTQJplTXkkr3z3Jgl0AAvwgAAI8zehQ-NJ79CQ64mE7BA"},
    "iran_dastnevis": {"name": "ایران سنس دستنویس | IRAN Sans DastNevis", "file_id": "BQACAgQAAxkBAAOgahzFOJc0n7KMVxDQ0P-X_KqW3ogAAv0gAAI8zehQRW-QnJKuG4I7BA"},
    "iran_sharp": {"name": "ایران شارپ | IRAN Sharp", "file_id": "BQACAgQAAxkBAAOhahzFOBSbvvGsPHvM9xVJsKyrdMgAAv4gAAI8zehQMNrt-FSLoTc7BA"},
    "javan": {"name": "جوان | Javan", "file_id": "BQACAgQAAxkBAAOiahzFOHsa81_k0BO6rKacxYCWaWEAAv8gAAI8zehQPSmS34lnfBs7BA"},
    "kamva": {"name": "کاموا | Kamva", "file_id": "BQACAgQAAxkBAAOjahzFOKJvz26BrJ4tZDLBz86q2QcAAyEAAjzN6FC8tZ19y6uX4jsE"},
    "katibeh": {"name": "کتیبه | Katibeh", "file_id": "BQACAgQAAxkBAAOkahzFOKIF9GjVZ9tb78PD-sjHQQ8AAgEhAAI8zehQTfgWFBliAtY7BA"},
    "kennar": {"name": "کنار | Kennar", "file_id": "BQACAgQAAxkBAAOlahzFOB9wyRV5aJ5jbApz14gIqI4AAgIhAAI8zehQC0dHyQxRhik7BA"},
    "mahboubeh": {"name": "محبوبه مهرآور | Mahboubeh Mehravar", "file_id": "BQACAgQAAxkBAAOmahzFOJvGDAvoNwYs8UWSpXWWNdMAAgMhAAI8zehQnZSs-9TPaWA7BA"},
    "pelak": {"name": "پلاک | Pelak", "file_id": "BQACAgQAAxkBAAOnahzFOM0n-T-divqxM85g9-zMXg8AAgQhAAI8zehQiYr0TPnaNos7BA"},
    "roosta": {"name": "روستا | Roosta", "file_id": "BQACAgQAAxkBAAOoahzFOMkvXj8J-5Z0KLlcy50qdK4AAgUhAAI8zehQ0yuBnbZZBRc7BA"},
    "sedaghat": {"name": "صداقت | Sedaghat", "file_id": "BQACAgQAAxkBAAOpahzFOCr3JaUqqjTEJS63X-8qEekAAgYhAAI8zehQ1tQdO8sfc0M7BA"},
    "tahamtan": {"name": "تهمتن | Tahamtan", "file_id": "BQACAgQAAxkBAAO0ahzFTgABEfrw7O1Z1uxabs0wZ4y3AAIHIQACPM3oUCkWbYZeZW5EOwQ"},
    "tahrir": {"name": "تحریر | Tahrir", "file_id": "BQACAgQAAxkBAAO1ahzFTgsj2am4NcZ2SQwjxy50-wQAAgghAAI8zehQDW1rZuy8DAQ7BA"},
    "tajrid": {"name": "تجرید | Tajrid", "file_id": "BQACAgQAAxkBAAO2ahzFTiogG55DXG8HoGe_zrRtxToAAgkhAAI8zehQyhQpBY_6pNM7BA"},
    "titr_grafiti": {"name": "تیتر گرافیتی | Titr Graphiti", "file_id": "BQACAgQAAxkBAAO3ahzFTq1BERK5jQXEUSHyHejyemgAAgohAAI8zehQJS1vk05UX7E7BA"},
    "titr_zebr": {"name": "تیتر زبر | Titr Zebr", "file_id": "BQACAgQAAxkBAAO4ahzFTqkJlZ7S7_tHaC84L-GPr_0AAgshAAI8zehQjP2_gc5Jsjs7BA"},
}

async def is_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramError:
        return False

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 عضویت در کانال", url="https://t.me/designfont6")],
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
        "🎨 *دیزاین فونت*\n\n"
        "یه فونت انتخاب کن و دانلودش کن 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def send_font_file(message, font_key, context):
    font = FONTS.get(font_key)
    if not font:
        await message.reply_text("❌ فونت پیدا نشد!")
        return
    await message.reply_text(f"⏳ در حال ارسال *{font['name']}*...", parse_mode="Markdown")
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
    if update.effective_user.id != ADMIN_ID:
        return
    if update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
        await update.message.reply_text(
            f"✅ فایل دریافت شد!\n\n📁 نام: `{file_name}`\n🔑 File ID:\n`{file_id}`",
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
