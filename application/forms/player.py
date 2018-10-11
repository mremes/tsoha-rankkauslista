from flask_wtf import Form
from wtforms import StringField, validators, DateField, RadioField
from . import Player


class PlayerForm(Form):
    name = StringField(
        'Nimi', [validators.DataRequired(), validators.Length(min=6)])
    gender = RadioField('Sukupuoli', [validators.DataRequired()], choices=[
                        ('mies', 'mies'), ('nainen', 'nainen'), ('muu', 'muu')])
    dob = DateField('Syntymäaika (pp.kk.vvvv)', format="%d.%m.%Y")
    pob = StringField('Syntymäpaikka', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.player = kwargs.get('player')
        if self.player is not None and not self.is_submitted():
            self.name.default = self.player.name
            self.gender.default = self.player.gender
            self.dob.default = self.player.dateofbirth
            self.pob.default = self.player.placeofbirth
            self.process()

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if not self.player:
            user = Player.query.filter_by(name=self.name.data).first()
            if user is not None:
                self.name.errors.append('Pelaaja on jo olemassa.')
                return False
        return True
