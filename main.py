from flask import flask

from threading import Thread
import telebot

TOKEN = "8819285435:AAH10iB7jzjKTHh5QL4vzPZGI9OYH7o4NCo"

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "BOT RUNNING"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 VOIDXDOWNLOADER WORKING")

keep_alive()

print("BOT STARTED")

bot.infinity_polling()
