from flask_wtf import Form

from application.rankings import TournamentPlayer
from application.rankings.models import TournamentPrize
from application import db
from wtforms import IntegerField


class TournamentPrizesForm(Form):
    dyn_attrs = []

    def __init__(self, tournament, *args, **kwargs):
        self.tournament = tournament
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        for attr in self.dyn_attrs:
            if not getattr(self, attr).validate(self):
                return False
        return True

    @staticmethod
    def _init_dyn_attrs():
        for attr in TournamentPrizesForm.dyn_attrs:
            setattr(TournamentPrizesForm, attr, None)
        TournamentPrizesForm.dyn_attrs = []

    def create_prizes_fields(self):
        TournamentPrizesForm._init_dyn_attrs()
        num_players = self.tournament.get_num_players()

        for i in range(num_players):
            attr = 'p{}'.format(i)
            setattr(TournamentPrizesForm,
                    attr,
                    IntegerField('%d. sijoituksen palkinto' % (i + 1)))
            TournamentPrizesForm.dyn_attrs.append(attr)

    def create_prizes(self):
        prizes = []
        # Create tournament player pairs
        for i in range(len(self.dyn_attrs)):
            prize_money = getattr(self, self.dyn_attrs[i]).data
            prize = TournamentPrize(self.tournament, i + 1, prize_money)
            db.session().add(prize)
            prizes.append(prize)
        db.session().commit()
        return prizes

    def create_ranking_points_fields(self):
        TournamentPrizesForm._init_dyn_attrs()

        prizes = TournamentPrize.query.filter_by(tournament_id=self.tournament.id).all()

        for i, prize in enumerate(prizes):
            attr = 'p{}'.format(i)
            setattr(TournamentPrizesForm,
                    attr,
                    IntegerField(
                        '%d. sijoituksen ranking-pisteet (rahapalkinto: %s)' % (prize.position, prize.prize_money),
                        id=prize.position,
                        default=prize.ranking_points))
            TournamentPrizesForm.dyn_attrs.append(attr)

    def update_ranking_points(self):
        for attr in self.dyn_attrs:
            attr = getattr(self, attr)
            prize = TournamentPrize.query.filter_by(position=attr.id,
                                                    tournament_id=self.tournament.id).first()
            prize.ranking_points = attr.data
            db.session.commit()

    def create_tournament_results_fields(self):
        TournamentPrizesForm._init_dyn_attrs()

        prizes = TournamentPrize.query.filter_by(tournament_id=self.tournament.id).all()
        players = TournamentPlayer.query.filter_by(tournament_id=self.tournament.id).all()

        for i, prize in enumerate(prizes):
            attr = 'p{}'.format(i)
            setattr(TournamentPrizesForm,
                    attr,
                    SelectField(
                        '%d. sijoituksen ranking-pisteet (rahapalkinto: %s)' % (prize.position, prize.prize_money),
                        id=prize.position,
                        default=prize.ranking_points))
