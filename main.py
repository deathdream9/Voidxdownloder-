from flask import Flask
from threading import Thread
import telebot
from telebot import types
import yt_dlp
import requests
import random
import qrcode
from io import BytesIO
import os

# ================= SETTINGS =================

TOKEN = "8819285435:AAH10iB7jzjKTHh5QL4vzPZGI9OYH7o4NCo"
ADMIN_ID = 7547763921

OWNER_NAME = "DEATH DREAM"

CHANNEL_USERNAME = "HACKERQUEEN9"

TELEGRAM_LINK = "https://t.me/HACKERQUEEN9"
WHATSAPP_LINK = "https://whatsapp.com/channel/0029Vb7MViI0VycACP8CUI32"

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

⚡ VIDEO DOWNLOADER
⚡ PASSWORD GENERATOR
⚡ QR GENERATOR
⚡ WEATHER TOOL
⚡ CRYPTO TOOL

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
        f"📢 TELEGRAM : {TELEGRAM_LINK}

💬 WHATSAPP : {WHATSAPP_LINK}"
    )

# ================= STATUS =================

@bot.message_handler(func=lambda m: m.text == "⚡ STATUS")
def status(message):

    bot.reply_to(
        message,
        "✅ BOT ONLINE AND WORKING"
    )

# ================= PASSWORD =================

@bot.message_handler(commands=['password'])
def password(message):

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#"

    pwd = ''.join(random.choice(chars) for _ in range(12))

    bot.reply_to(message, f"🔐 PASSWORD:
{pwd}")

# ================= QR =================

@bot.message_handler(commands=['qr'])
def qr(message):

    try:
        text = message.text.replace('/qr ', '')

        img = qrcode.make(text)

        bio = BytesIO()
        bio.name = 'qr.png'

        img.save(bio, 'PNG')

        bio.seek(0)

        bot.send_photo(message.chat.id, bio)

    except:
        bot.reply_to(message, "Usage: /qr your text")

# ================= WEATHER =================

@bot.message_handler(commands=['weather'])
def weather(message):

    try:
        city = message.text.split()[1]

        data = requests.get(f'https://wttr.in/{city}?format=3').text

        bot.reply_to(message, data)

    except:
        bot.reply_to(message, "Usage: /weather karachi")

# ================= PING =================

@bot.message_handler(commands=['ping'])
def ping(message):

    bot.reply_to(message, "🏓 BOT ONLINE")

# ================= CRYPTO =================

@bot.message_handler(commands=['crypto'])
def crypto(message):

    try:
        coin = message.text.split()[1].lower()

        url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd'

        data = requests.get(url).json()

        price = data[coin]['usd']

        bot.reply_to(message, f'💰 {coin.upper()} PRICE : ${price}')

    except:
        bot.reply_to(message, 'Usage: /crypto bitcoin')

# ================= VIDEO DOWNLOADER =================

@bot.message_handler(func=lambda m: m.text.startswith("http"))
def downloader(message):

    url = message.text

    bot.reply_to(message, "⏳ DOWNLOADING VIDEO PLEASE WAIT...")

    try:

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(
                message.chat.id,
                video,
                caption="🔥 POWERED BY DARK HACKER ZONE 🔥"
            )

        os.remove(filename)

    except Exception as e:

        bot.reply_to(message, f"❌ ERROR : {e}")

# ================= ADMIN =================

@bot.message_handler(commands=['admin'])
def admin(message):

    if message.from_user.id != ADMIN_ID:
        return

    bot.reply_to(message, "👑 ADMIN PANEL ACTIVE")

# ================= START BOT =================

keep_alive()

print("BOT STARTED")

bot.infinity_polling()
