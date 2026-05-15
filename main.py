from flask import Flask
from threading import Thread
import telebot
from telebot import types

# ================= SETTINGS =================

TOKEN = "8819285435:AAH10iB7jzjKTHh5QL4vzPZGI9OYH7o4NCo"

ADMIN_ID = 7547763921

CHANNEL_USERNAME = "HACKERQUEEN9"

TELEGRAM_LINK = "https://t.me/HACKERQUEEN9"

WHATSAPP_LINK = "https://whatsapp.com/channel/0029Vb7MViI0VycACP8CUI32"

OWNER_NAME = "DEATH DREAM"

bot = telebot.TeleBot(TOKEN)

# ================= FLASK =================

app = Flask(__name__)

@app.route('/')
def home():
    return "VOIDXDOWNLOADER BOT RUNNING"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ================= FORCE JOIN =================

def check_join(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)

        if member.status in ["member", "administrator", "creator"]:
            return True

    except:
        return False

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id

    if not check_join(user_id):

        markup = types.InlineKeyboardMarkup()

        btn1 = types.InlineKeyboardButton(
            "📢 JOIN TELEGRAM",
            url=TELEGRAM_LINK
        )

        btn2 = types.InlineKeyboardButton(
            "💬 JOIN WHATSAPP",
            url=WHATSAPP_LINK
        )

        markup.add(btn1)
        markup.add(btn2)

        bot.reply_to(
            message,
            "⚠️ FIRST JOIN CHANNELS TO USE BOT",
            reply_markup=markup
        )

        return

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

    b1 = types.KeyboardButton("📥 DOWNLOAD")
    b2 = types.KeyboardButton("👑 OWNER")
    b3 = types.KeyboardButton("📢 CHANNEL")
    b4 = types.KeyboardButton("⚡ STATUS")

    menu.add(b1, b2)
    menu.add(b3, b4)

    text = f"""
🔥 WELCOME TO VOIDXDOWNLOADER 🔥

👑 OWNER : {OWNER_NAME}

⚡ FAST VIDEO DOWNLOADER

📢 TELEGRAM :
{TELEGRAM_LINK}

💬 WHATSAPP :
{WHATSAPP_LINK}

SEND VIDEO LINK TO DOWNLOAD

🔥 POWERED BY DARK HACKER ZONE
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=menu
    )

# ================= OWNER =================

@bot.message_handler(func=lambda m: m.text == "👑 OWNER")
def owner(message):

    bot.reply_to(
        message,
        f"👑 OWNER NAME : {OWNER_NAME}"
    )

# ================= CHANNEL =================

@bot.message_handler(func=lambda m: m.text == "📢 CHANNEL")
def channel(message):

    bot.reply_to(
        message,
        f"📢 TELEGRAM : {TELEGRAM_LINK}\n\n💬 WHATSAPP : {WHATSAPP_LINK}"
    )

# ================= STATUS =================

@bot.message_handler(func=lambda m: m.text == "⚡ STATUS")
def status(message):

    bot.reply_to(
        message,
        "✅ BOT ONLINE AND WORKING"
    )

# ================= DOWNLOAD =================

@bot.message_handler(func=lambda m: m.text == "📥 DOWNLOAD")
def download(message):

    bot.reply_to(
        message,
        "📥 SEND VIDEO LINK"
    )

# ================= LINK DETECT =================

@bot.message_handler(func=lambda m: "http" in m.text)
def links(message):

    bot.reply_to(
        message,
        "⚡ VIDEO DOWNLOADER COMING SOON\n\n🔥 POWERED BY DARK HACKER ZONE"
    )

# ================= ADMIN =================

@bot.message_handler(commands=['admin'])
def admin(message):

    if message.from_user.id != ADMIN_ID:
        return

    bot.reply_to(
        message,
        "👑 ADMIN PANEL ACTIVE"
    )

# ================= START BOT =================

keep_alive()

print("BOT STARTED")

bot.infinity_polling()
