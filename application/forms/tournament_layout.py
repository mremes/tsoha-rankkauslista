from flask_wtf import Form
from application.rankings.models import RankingList, Tournament, TournamentPlayer, Player, Match
from application import db
from wtforms import SelectField


class TournamentLayoutForm(Form):
    dyn_attrs = []

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        return True

    def get_tournament_object(self):
        return Tournament(self.name.data,
                          self.venue.data,
                          self.date.data,
                          self.ranking_list.data)

    @staticmethod
    def update_form_fields(num_players, ranking_list):
        for attr in TournamentLayoutForm.dyn_attrs:
            setattr(TournamentLayoutForm, attr, None)
        TournamentLayoutForm.dyn_attrs = []
        choices = [(p.id, p.name) for p in ranking_list.players]
        for i in range(int(num_players/2)):
            for j in range(2):
                tpl = (i + 1), (j + 1)
                attr = 'm{}p{}'.format(*tpl)
                setattr(TournamentLayoutForm,
                        attr,
                        SelectField('Ottelupari %d, pelaaja %d' % tpl, choices=choices))
                TournamentLayoutForm.dyn_attrs.append(attr)

    def create_matches(self, tournament):
        pairs = []
        # Create tournament player pairs
        for i in range(len(self.dyn_attrs)):
            if i % 2 == 0:
                player1id = getattr(self, self.dyn_attrs[i]).data
                player1 = Player.query.get(player1id)
                tplayer1 = TournamentPlayer(tournament, player1)
                player2id = getattr(self, self.dyn_attrs[i+1]).data
                player2 = Player.query.get(player2id)
                tplayer2 = TournamentPlayer(tournament, player2)
                db.session().add(tplayer1)
                db.session().add(tplayer2)
                pairs.append(tuple((tplayer1, tplayer2)))
        # Create tournament matches
        matches = []
        for pair in pairs:
            player1, player2 = pair
            match = Match(tournament, player1, player2)
            db.session().add(match)
            matches.append(match)
        db.session().commit()
        del pairs
        return matches
