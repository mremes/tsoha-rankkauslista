import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.extensions import csrf

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(32)

csrf.init_app(app)

if os.environ.get('HEROKU'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rankings.db'
    app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

from application import views

from application.rankings import models
from application.rankings import views

from application.auth import models
from application.auth import views

# noinspection PyBroadException
try:
    db.create_all()
except Exception as ex:
    pass

from application.auth.login import login_manager

login_manager.init_app(app)
