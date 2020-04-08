from pytube import YouTube
from telegram.ext import Updater, CommandHandler
from youtube_search import YoutubeSearch
import os

# initialising
token = open("config.txt", "r").read().strip()
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
PATH = "./tmpdl/"


def createAnswer(keywords, isQuickplay):
    terms = ' '.join([word for word in keywords])
    results = YoutubeSearch(terms, max_results=1).to_dict()
    name = results[0]["title"]
    link = "https://www.youtube.com" + results[0]["link"]
    answer = f"Here is {name}: {link}"
    if isQuickplay:
        return link
    else:
        return answer


def quickplay(update, context):
    link = createAnswer(context.args, True)
    yt = YouTube(link)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first()
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    yt.download(PATH)
    context.bot.send_video(
        chat_id=update.message.chat_id, video=open(PATH + yt.title + ".mp4", "rb"), supports_streaming=True)
    os.remove(PATH + yt.title + ".mp4")


def play(update, context):
    answer = createAnswer(context.args, False)
    context.bot.send_message(
        chat_id=update.message.chat_id, text=answer)


def dl(update, context):
    if(len(context.args[0]) > 1):
        yt = YouTube(context.args[0])
        context.bot.send_message(
            chat_id=update.message.chat_id, text=f"Downloading {yt.title}")
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id, text="No link found!")
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first()
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    yt.download(PATH)
    context.bot.send_video(
        chat_id=update.message.chat_id, video=open(PATH + yt.title + ".mp4", "rb"), supports_streaming=True)
    os.remove(PATH + yt.title + ".mp4")


# start polling
dispatcher.add_handler(CommandHandler("play", play))
dispatcher.add_handler(CommandHandler("dl", dl))
dispatcher.add_handler(CommandHandler("quickplay", quickplay))
updater.start_polling()
