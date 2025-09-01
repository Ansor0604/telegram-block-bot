import os
import pytz
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import timedelta, datetime

UZBEK_TZ = pytz.timezone('Asia/Tashkent')

# So'kinish va haqoratli so'zlar ro'yxati (uzb, rus, ingliz)
BAD_WORDS = [
    # Uzbekcha
    "ahmoq", "tentak", "yaramas", "it", "onangni", "oneyni", "jinni", "ske",
    "la'nati", "qotaq", "qoto", "qo'to", "o'lgur", "ochko'z", "beodob", "kot", "dinnaxuy" ,"dinnahuy", "idinaxuy", "idinahuy",
    "kotmisan", "ko'tmisan", "ko'tbo'ma", "kotboma", "am", "opangni", "pasholnaxuy", "pawol", "pashol", "pwl", "pshl",
    "kotini", "seks", "skibdi", "skaman", "ceks", "naxuy"


    # Ruscha (qisqartirilgan misollar)
    "durak", "tvar", "ublydok", "svoloch", "blet", "pidaraz", "maraz",
    "kozel", "dalbayop", "shly*xa", "xuyet", "huyet", "huyetqivosami", "xuyetqivosami", "huyetqivosanmi", "xuyetqivosanmi",
    "qotagimi", "qo'tag'imi", "qotag'imi", "yiban", "yobana", "yibanoti", "yban", "ybanoti", "sike", "sik", "sikib", "sikibdi", "sikibdimi", 
    "кот", "хуй", "хуя", "пизда", "пиздец", "ебать", "ебал", "ебан", "еблан", "ебаный", "ебаныйвтвоюматерь", "ебаныйвтвоюмать", 
    "далбайоп", "ске", "секс", "чумо", "чмо", "пидар", "пидорас", "пидорасина", "пидорасня", "пидарасина", "пидарасня",
    "бле", "вай бле", "вайбле", "блядь", "бля", "твар"

    # Inglizcha
    "idiot", "stupid", "fool", "bastard", "moron", "loser",
    "fuck", "shit", "bitch", "asshole", "jerk", "slut", "dick"
]

# Vaqtli bloklash muddati (masalan: 1 soat)
BAN_TIME = timedelta(hours=1)

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id

        admins = [admin.user.id for admin in await context.bot.get_chat_administrators(chat_id)]

        text = update.message.text.lower()

        # Agar xabarda taqiqlangan so'z bo'lsa
        if any(word in text for word in BAD_WORDS):
            user_id in admins
            await update.message.reply_text("❗ Admin bo'lsangiz ham so'kinmang. Robbingizdan hayo qiling")
        else:
            await context.bot.ban_chat_member(chat_id, user_id)
            await update.message_reply_text("🚫 So‘kinish taqiqlangan! Siz bloklandingiz.")

            # Ban muddati (hozirgi vaqt + BAN_TIME)
            until_date = datetime.now() + BAN_TIME

            try:
                await context.bot.ban_chat_member(chat_id, user_id, until_date=until_date)
                await update.message.reply_text(
                    f"🚫 So‘kinish taqiqlangan!\n"
                    f"👤 {update.message.from_user.first_name} "
                    f"{BAN_TIME.total_seconds()/60:.0f} daqiqaga bloklandi."
                )
            except Exception as e:
                await update.message.reply_text("❌ Foydalanuvchini bloklashda xatolik yuz berdi.")
                print(e)

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))

    app.job_queue.scheduler.configure(timezone=pytz.UTC)

    print("✅ Bot ishlayapti...")
    app.run_polling()

if __name__ == "__main__":
    main()
