from flask_wtf import Form
from wtforms import StringField, validators, DateField, RadioField
from . import Player


class PlayerForm(Form):
    name = StringField('Käyttäjätunnus', [validators.DataRequired(), validators.Length(min=6)])
    gender = RadioField('Sukupuoli', [validators.DataRequired()], choices=[("mies", "male"), ("nainen", "female"), ("muu", "other")])
    dob = DateField('Syntymäaika (pp.kk.vvvv)', [validators.DataRequired()], format='%d.%m.%Y')
    pob = StringField('Syntymäpaikka', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Player.query.filter_by(name=self.name.data).first()
        if user is not None:
            self.name.errors.append('Pelaaja on jo olemassa')
            return False

        self.user = user
        return True
