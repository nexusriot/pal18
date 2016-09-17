#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import telebot
import logging
import yaml

from bot_api.db_api import db, app, BotRequest


# todo: refactor me
with open("config.yml", "r") as config_file:
    cfg = yaml.load(config_file)

# todo: move to the config loader
API_TOKEN = cfg['bot']['api_token']
WEBHOOK_HOST = cfg['server']['host']
WEBHOOK_PORT = cfg['server']['port']
WEBHOOK_LISTEN = cfg['server']['listen']
WEBHOOK_SSL_CERT = cfg['server']['ssl_cert']
WEBHOOK_SSL_PRIV = cfg['server']['ssl_key']

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % API_TOKEN


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)


# Empty web server index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'hello'


# Process web hook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def web_hook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().encode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_messages([update.message])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['history'])
def handle_requests_history_command(message):
    history = BotRequest.get_history(message.from_user.id)
    bot.send_message(message.from_user.id,
                     history)


@bot.message_handler(commands=['start'])
def handle_help_command(message):
        bot.send_message(message.from_user.id,
                         "Hey, %s" % message.from_user.first_name)


# Handle '/help'
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.from_user.id,
                     ("Hi, I am Pal 18 bot!.\n"
                      "I don't like you, %s" % message.from_user.first_name))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_info(message):
    request = BotRequest(message)
    request.db_save()
    bot.send_message(message.from_user.id,
                     str(message))


def main():
    # create database
    db.create_all()
    # Remove web hook, it fails sometimes the set if there is a previous webhook
    bot.remove_webhook()

    # Set web hook
    bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    # Start server
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=True)


if __name__ == '__main__':
    main()
