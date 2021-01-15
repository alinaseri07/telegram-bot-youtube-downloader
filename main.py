import os
import telebot
from pytube import YouTube
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, send my your youtube link?")


@bot.message_handler()
def function_name(message):
    print(message)
    streams = []
    try:
        yt = YouTube(message.text)
    except:
        bot.send_message(message.chat.id, 'Invalid URL')
        return

    bot.send_message(message.chat.id, 'Downloading...')
    streams = yt.streams.filter(progressive=True).order_by('resolution')

    for stream in streams:
        path = stream.download(output_path="downloads/",
                               filename=stream.title + " - " + stream.resolution)

        video = open(path, 'rb')
        print(video)
        bot.send_video(message.chat.id, video, timeout=1000)
        os.remove("./downloads/" + stream.title +
                  " - " + stream.resolution + ".mp4")

    bot.send_message(message.chat.id, 'Done')


bot.polling()
