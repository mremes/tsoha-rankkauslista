from flask_wtf import Form
from flask import flash

from application.rankings.models import RankingList, Ranking
from application.tournaments.models import Tournament, TournamentPlayer, TournamentPrize, Match
from application.players.models import Player
from application import db
from wtforms import SelectField


class TournamentLayoutForm(Form):
    dyn_attrs = []

    def __init__(self, tournament, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.tournament = tournament

    def validate(self):
        current_players = set()
        for dyn_attr in self.dyn_attrs:
            pid = getattr(self, dyn_attr).data
            if pid in current_players:
                flash('Samaa pelaajaa ei voi asetella useampaan kertaan.')
                return False
            current_players.add(pid)
        return True

    @staticmethod
    def _init_dyn_attrs():
        for attr in TournamentLayoutForm.dyn_attrs:
            setattr(TournamentLayoutForm, attr, None)
        TournamentLayoutForm.dyn_attrs = []

    def get_tournament_object(self):
        return Tournament(self.name.data,
                          self.venue.data,
                          self.date.data,
                          self.ranking_list.data)

    def update_layout_fields(self):
        TournamentLayoutForm._init_dyn_attrs()
        ranking_list = RankingList.query.get(self.tournament.ranking_list_id)
        ranking_list.populate_players()
        num_players = len(Ranking.query.filter_by(list_id=ranking_list.id).all())

        choices = [(p.id, p.name) for p in ranking_list.players]
        for i in range(int(num_players/2)):
            for j in range(2):
                tpl = (i + 1), (j + 1)
                attr = 'm{}p{}'.format(*tpl)
                setattr(TournamentLayoutForm,
                        attr,
                        SelectField('Ottelupari %d, pelaaja %d' % tpl, choices=choices))
                TournamentLayoutForm.dyn_attrs.append(attr)

    def create_matches(self):
        pairs = []
        # Create tournament player pairs
        for i in range(len(self.dyn_attrs)):
            if i % 2 == 0:
                player1id = getattr(self, self.dyn_attrs[i]).data
                player1 = Player.query.get(player1id)
                tplayer1 = TournamentPlayer(self.tournament, player1)
                player2id = getattr(self, self.dyn_attrs[i+1]).data
                player2 = Player.query.get(player2id)
                tplayer2 = TournamentPlayer(self.tournament, player2)
                db.session().add(tplayer1)
                db.session().add(tplayer2)
                db.session().commit()
                pairs.append([tplayer1, tplayer2])
        # Create tournament matches
        matches = []
        for pair in pairs:
            player1, player2 = pair
            match = Match(self.tournament, player1, player2)
            db.session().add(match)
            matches.append(match)
        db.session().commit()
        del pairs
        return matches

    def update_standings_fields(self):
        TournamentLayoutForm._init_dyn_attrs()
        tplayers = TournamentPlayer.query.filter_by(tournament_id=self.tournament.id)
        players = Player.query.filter(Player.id.in_([p.player_id for p in tplayers])).all()
        choices = [(p.id, p.name) for p in players]
        prizes = TournamentPrize.query.filter_by(tournament_id=self.tournament.id).order_by(TournamentPrize.position).all()

        for prize in prizes:
            attr = 'p{}'.format(prize.position)
            setattr(TournamentLayoutForm,
                    attr,
                    SelectField('%s. sija' % prize.position,
                                id=prize.id,
                                default=prize.player_id,
                                choices=choices))
            TournamentLayoutForm.dyn_attrs.append(attr)

    def update_prizes(self):
        for a in self.dyn_attrs:
            attr = getattr(self, a)
            prize = TournamentPrize.query.get(attr.id)
            prize.player_id = attr.data
            db.session.commit()
