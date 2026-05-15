`main.pay` ko rename karke `main.py` kar do, phir usme yeh updated code paste karo.

```python id="8t1jsh"
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

# ================= BOT SETTINGS =================

TOKEN = "8819285435:AAH10iB7jzjKTHh5QL4vzPZGI9OYH7o4NCo"

OWNER = "DEATH DREAM"

CHANNEL_USERNAME = "HACKERQUEEN9"

CHANNEL_LINK = "https://t.me/HACKERQUEEN9"

WHATSAPP_LINK = "https://whatsapp.com/channel/0029Vb7MViI0VycACP8CUI32"

ADMIN_ID = 7547763921

bot = telebot.TeleBot(TOKEN)

# ================= UPTIME / FLASK =================

app = Flask(__name__)

@app.route('/')
def home():
    return "VOIDXDOWNLOADER BOT IS RUNNING"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ================= FORCE JOIN =================

def check_sub(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)

        if member.status in ['member', 'administrator', 'creator']:
            return True

    except:
        return False

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id

    if not check_sub(user_id):

        markup = types.InlineKeyboardMarkup()

        btn1 = types.InlineKeyboardButton(
            "📢 JOIN TELEGRAM",
            url=CHANNEL_LINK
        )

        btn2 = types.InlineKeyboardButton(
            "💬 JOIN WHATSAPP",
            url=WHATSAPP_LINK
        )

        markup.add(btn1)
        markup.add(btn2)

        bot.reply_to(
            message,
            "⚠️ FIRST JOIN OUR CHANNELS TO USE THIS BOT",
            reply_markup=markup
        )

        return

    photo = "https://i.imgur.com/3ZQ3Z6Q.jpeg"

    text = f"""
🔥 WELCOME TO VOIDXDOWNLOADER 🔥

👑 OWNER : {OWNER}

⚡ FAST VIDEO DOWNLOADER
⚡ YOUTUBE DOWNLOADER
⚡ TIKTOK DOWNLOADER
⚡ INSTAGRAM DOWNLOADER

📢 TELEGRAM :
{CHANNEL_LINK}

💬 WHATSAPP :
{WHATSAPP_LINK}

SEND VIDEO LINK TO DOWNLOAD
"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    b1 = types.KeyboardButton("📥 DOWNLOAD")
    b2 = types.KeyboardButton("👑 OWNER")
    b3 = types.KeyboardButton("📢 CHANNELS")
    b4 = types.KeyboardButton("🛠 TOOLS")

    markup.add(b1, b2)
    markup.add(b3, b4)

    bot.send_photo(
        message.chat.id,
        photo,
        caption=text,
        reply_markup=markup
    )

# ================= CHANNELS =================

@bot.message_handler(func=lambda m: m.text == "📢 CHANNELS")
def channels(message):

    bot.reply_to(
        message,
        f"📢 TELEGRAM:\n{CHANNEL_LINK}\n\n💬 WHATSAPP:\n{WHATSAPP_LINK}"
    )

# ================= OWNER =================

@bot.message_handler(func=lambda m: m.text == "👑 OWNER")
def owner(message):

    bot.reply_to(
        message,
        f"👑 OWNER NAME : {OWNER}"
    )

# ================= TOOLS =================

@bot.message_handler(func=lambda m: m.text == "🛠 TOOLS")
def tools(message):

    text = """
🛠 AVAILABLE TOOLS

/password
/ip
/qr
/weather
/ping
/crypto
"""

    bot.reply_to(message, text)

# ================= PASSWORD =================

@bot.message_handler(commands=['password'])
def password(message):

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#"

    pwd = ''.join(random.choice(chars) for _ in range(12))

    bot.reply_to(
        message,
        f"🔐 PASSWORD:\n{pwd}"
    )

# ================= IP LOOKUP =================

@bot.message_handler(commands=['ip'])
def ip_lookup(message):

    try:
        ip = message.text.split()[1]

        data = requests.get(
            f"http://ip-api.com/json/{ip}"
        ).json()

        text = f"""
🌍 IP LOOKUP

IP : {data['query']}
COUNTRY : {data['country']}
CITY : {data['city']}
ISP : {data['isp']}
TIMEZONE : {data['timezone']}
"""

        bot.reply_to(message, text)

    except:
        bot.reply_to(
            message,
            "USAGE : /ip 8.8.8.8"
        )

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
        bot.reply_to(
            message,
            "USAGE : /qr your text"
        )

# ================= WEATHER =================

@bot.message_handler(commands=['weather'])
def weather(message):

    try:
        city = message.text.split()[1]

        url = f'https://wttr.in/{city}?format=3'

        data = requests.get(url).text

        bot.reply_to(message, data)

    except:
        bot.reply_to(
            message,
            "USAGE : /weather karachi"
        )

# ================= PING =================

@bot.message_handler(commands=['ping'])
def ping(message):

    bot.reply_to(
        message,
        "🏓 PONG BOT ONLINE"
    )

# ================= CRYPTO =================

@bot.message_handler(commands=['crypto'])
def crypto(message):

    try:
        coin = message.text.split()[1].lower()

        url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd'

        data = requests.get(url).json()

        price = data[coin]['usd']

        bot.reply_to(
            message,
            f"💰 {coin.upper()} PRICE : ${price}"
        )

    except:
        bot.reply_to(
            message,
            "USAGE : /crypto bitcoin"
        )

# ================= VIDEO DOWNLOADER =================

@bot.message_handler(func=lambda message: "http" in message.text)
def download_video(message):

    url = message.text

    bot.reply_to(
        message,
        "⏳ DOWNLOADING VIDEO..."
    )

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s'
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            filename = ydl.prepare_filename(info)

        caption = "🔥 POWERED BY DARK HACKER ZONE 🔥"

        with open(filename, 'rb') as video:

            bot.send_video(
                message.chat.id,
                video,
                caption=caption
            )

        os.remove(filename)

    except Exception as e:

        bot.reply_to(
            message,
            f"❌ ERROR : {e}"
        )

# ================= ADMIN =================

@bot.message_handler(commands=['admin'])
def admin(message):

    if message.from_user.id != ADMIN_ID:
        return

    text = """
👑 ADMIN PANEL

/broadcast
/ping
"""

    bot.reply_to(message, text)

# ================= START BOT =================

keep_alive()

print("VOIDXDOWNLOADER BOT RUNNING")

bot.infinity_polling()
```
