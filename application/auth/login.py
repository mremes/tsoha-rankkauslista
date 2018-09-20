import flask_login
from .models import User
from application import db

login_manager = flask_login.LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return db.session().query(User).filter_by(id=user_id).first()


def login_user(*args, **kwargs):
    return flask_login.login_user(*args, **kwargs)


def logout_user():
    return flask_login.logout_user()
