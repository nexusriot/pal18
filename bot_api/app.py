#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
