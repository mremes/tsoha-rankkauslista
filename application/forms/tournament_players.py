from flask_wtf import Form
from wtforms import validators, SelectField, HiddenField


class TournamentPlayersForm(Form):
    tournament_id = HiddenField('TournamentId', [validators.DataRequired()])
    num_players = SelectField('Pelaajien lukumäärä', choices=[(2**x, 2**x)
                                                              for x in range(1, 8)])

    def __init__(self, tournament_id, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.tournament_id.default = tournament_id

    def validate(self):
        return True
