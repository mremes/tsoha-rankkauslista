import math

from application.rankings.models import RankingList
from flask_wtf import Form
from wtforms import SelectField
from application.forms.extensions import HiddenField


class TournamentPlayersForm(Form):
    tournament_id = HiddenField('TournamentId')
    num_players = SelectField('Pelaajien lukumäärä', coerce=int)

    def __init__(self, tournament, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.tournament_id.default = tournament.id

        rl = RankingList.query.get(tournament.ranking_list_id)
        rl.populate_players()
        num_players = len(rl.players)
        num_players_cap = [(num_players, x) for x in range(1, 8) if num_players - 2**x >= 0][-1][1]
        self.num_players.choices = [(2 ** x, 2 ** x) for x in range(1, num_players_cap+1)]
