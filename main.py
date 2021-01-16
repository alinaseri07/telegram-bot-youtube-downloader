import os
import uuid
import requests
import telebot
from pytube import YouTube
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, send me your youtube link plz")


@bot.message_handler()
def function_name(message):
    try:
        yt = YouTube(message.text)
    except:
        bot.send_message(message.chat.id, 'Invalid URL')
        return

    stream = yt.streams.filter(progressive=True).order_by('resolution').first()

    if (round((stream.filesize / 1024) / 1024) < 50):
        bot.send_message(message.chat.id, 'Downloading...')
        filename = uuid.uuid4().hex
        path = stream.download(output_path="downloads/",
                               filename=filename)

        video = open(path, 'rb')
        try:
            bot.send_video(message.chat.id, video, timeout=1000,
                           supports_streaming=True, width=640, height=360)
        except:
            bot.send_message(message.chat.id, 'Video size is too large')

        os.remove("./downloads/" + filename + ".mp4")

        bot.send_message(message.chat.id, 'Done')
    else:
        bot.send_message(message.chat.id, 'Video size is too large')


bot.polling()
