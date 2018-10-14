from flask_wtf import Form
from application.rankings.models import RankingList, Tournament
from wtforms import StringField, validators, SelectField, DateField


class TournamentInfoForm(Form):
    name = StringField(
        'Nimi', [validators.DataRequired(), validators.Length(min=2, max=60, message="Nimen pitää olla 2-60 merkkiä pitkä")])
    venue = StringField(
        'Paikka', [validators.DataRequired(), validators.Length(min=2, max=60, message="Paikan nimen pitää olla 2-60 merkkiä pitkä")])
    date = DateField('Aika (pp.kk.vvvv)', [validators.DataRequired(message="Pakollinen kenttä.")], format="%d.%m.%Y")
    ranking_list = SelectField('Ranking-lista', [validators.DataRequired(message="Pakollinen kenttä.")], choices=[])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not self.name.validate(self):
            return False
        if not self.venue.validate(self):
            return False
        if not self.date.validate(self):
            return False

        list_choices = [rlist.id for rlist in RankingList.query.all()]
        if not self.ranking_list.data not in list_choices:
            return False

        return True

    def get_tournament_object(self):
        return Tournament(self.name.data,
                          self.venue.data,
                          self.date.data,
                          self.ranking_list.data)
