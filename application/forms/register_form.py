from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from . import User


class RegisterForm(Form):
    name = StringField('Nimi', [validators.DataRequired()])
    username = StringField('Käyttäjätunnus', [validators.DataRequired(), validators.Length(min=6)])
    password = PasswordField('Salasana', [validators.Length(min=6), validators.EqualTo('confirm', message='Salasanojen pitää olla samat')])
    confirm = PasswordField('Salasana uudelleen', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is not None:
            self.username.errors = ['Käyttäjä on jo olemassa.']
            return False

        return True
