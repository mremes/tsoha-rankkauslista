# -*- coding: utf-8 -*-
import os

from flask import Flask, flash, url_for, redirect
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(32)

if os.environ.get('HEROKU'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rankings.db'
    app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# roles in login_required
from functools import wraps


def login_required(roles=None):
    if roles is None:
        roles = ["ANY"]

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            unauthorized = False

            if "ANY" not in roles:
                unauthorized = True

                for user_role in current_user.roles():
                    if user_role in roles:
                        unauthorized = False
                        break

            if unauthorized:
                flash('Sinulla ei ole oikeuksia käyttää tätä toiminnallisuutta.')
                return redirect(url_for('index'))

            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


from application import views

from application.players import models
from application.players import views
from application.rankings import models
from application.rankings import views
from application.tournaments import models
from application.tournaments import views

from application.auth.models import user
from application.auth import views

# noinspection PyBroadException
try:
    db.create_all()
except Exception as ex:
    pass

from application.auth.login import login_manager
login_manager.init_app(app)

from application.extensions import csrf

csrf.init_app(app)
