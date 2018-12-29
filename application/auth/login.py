# -*- coding: utf-8 -*-
import flask_login
from application.auth.models.user import User
login_manager = flask_login.LoginManager()

login_manager.login_view = 'login'
login_manager.login_message = 'Kirjaudu sisään käyttääksesi tätä toiminnallisuutta.'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def login_user(*args, **kwargs):
    return flask_login.login_user(*args, **kwargs)


def logout_user():
    return flask_login.logout_user()
