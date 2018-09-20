from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from . import User


class LoginForm(Form):
    username = StringField('Käyttäjätunnus', [validators.DataRequired(), validators.Length(min=6)])
    password = PasswordField('Salasana', [validators.DataRequired(), validators.Length(min=6)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
           return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Käyttäjätunnusta ei löydy')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Väärä salasana')
            return False

        self.user = user
        return True
