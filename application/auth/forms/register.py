from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, validators
from application.auth.models import User


class RegisterForm(Form):
    name = StringField('Nimi', [validators.DataRequired(message="Nimi ei saa olla tyhjä"),
                                validators.Length(min=2, max=60,
                                                  message="Nimen pitää olla vähintään 2 ja enintään 60 merkkiä pitkä.")],
                       render_kw={'maxlength': 60})
    username = StringField(
        'Käyttäjätunnus', [validators.DataRequired(),
                           validators.Length(min=6,
                                             max=20,
                                             message="Käyttäjätunnuksen pitää olla vähintään 6 ja enintään 20 merkkiä pitkä.")],
        render_kw={'maxlength': 20})
    role = RadioField("Rooli",
                      choices=[("ADMIN", "Ylläpitäjä"), ("PLAYER", "Pelaaja-agentti"), ("TOURNAMENT", "Turnausjärjestäjä")])
    password = PasswordField('Salasana', [validators.Length(
        min=6, max=50, message="Salasanan pitää olla vähintään 6 ja enintään 50 merkkiä pitkä."),
        validators.EqualTo('confirm', message='Salasanojen pitää olla samat.')])
    confirm = PasswordField('Salasana uudelleen', [validators.DataRequired(message="Vahvista salasana.")])

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
