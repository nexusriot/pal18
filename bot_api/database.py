# -*- coding: utf-8 -*-
import datetime
from sqlalchemy.orm import relationship
from app import db


class BotRequest(db.Model):

    __tablename__ = 'bot_request'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    text = db.Column('text', db.Text, nullable=False, default='')
    time = db.Column('time', db.DateTime, nullable=False,
                     default=datetime.datetime.utcnow())
    user_id = db.Column('user_id', db.Integer, nullable=False)
    user_name = db.Column('user_name', db.String(255), nullable=False,
                          default='')
    date = db.Column('date', db.Integer, nullable=False, default=0)
    first_name = db.Column('first_name', db.String(255), nullable=True)
    last_name = db.Column('last_name', db.String(255), nullable=True)

    def __init__(self, text, user_id, user_name, date=None,
                 first_name=None, last_name=None):
        self.text = text
        self.user_id = user_id
        self.user_name = user_name
        self.date = date
        self.first_name = first_name
        self.last_name = last_name


class Link(db.Model):

    __tablename__ = 'link'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    bot_request_id = db.Column('bot_request_id', db.ForeignKey('bot_request.id'),
                               index=True, nullable=False)
    text = db.Column('text', db.Text, nullable=False, default='')
    time = db.Column('time', db.DateTime, nullable=False,
                     default=datetime.datetime.utcnow())
    request = relationship('BotRequest')

    def __init__(self, bot_request_id, text):
        self.bot_request_id = bot_request_id
        self.text = text
