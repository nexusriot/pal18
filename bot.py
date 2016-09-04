# -*- coding: utf-8 -*-

import datetime
import telebot
from bot_api.config import token


bot = telebot.TeleBot(token, threaded=False)


@bot.message_handler(commands=['help'])
def handle_help_command(message):
    bot.send_message(message.from_user.id, """
    /start - Start the bot\n""")


@bot.message_handler(commands=['start'])
def handle_help_command(message):
    bot.send_message(message.from_user.id, "Started")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'date':
        bot.send_message(message.from_user.id,
                         datetime.datetime.now())


bot.polling(none_stop=True, interval=1)
