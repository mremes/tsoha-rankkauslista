from flask_wtf import Form
from wtforms import StringField, validators, RadioField, DateField
from application.players.models import Player
from application.forms.extensions import TranslatedForm


class PlayerForm(TranslatedForm):
    name = StringField(
        'Nimi', [validators.DataRequired(),
                 validators.Length(min=2, max=60, message="Nimi on vähintään 2 ja enintään 60 merkkiä pitkä.")])
    gender = RadioField('Sukupuoli', [validators.DataRequired(message="Valitse sukupuoli")], choices=[
        ('mies', 'mies'), ('nainen', 'nainen'), ('muu', 'muu')])
    dob = DateField('Syntymäaika (pp.kk.vvvv)', format="%d.%m.%Y")
    pob = StringField('Syntymäpaikka', [validators.DataRequired("Syötä syntymäaika"), validators.Length(min=2, max=70, message="Vähintään 2 ja enintään 70 merkkiä.")])

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
                self.name.errors = ['Pelaaja on jo olemassa.']
                return False
        return True
