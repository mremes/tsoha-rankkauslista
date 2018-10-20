from application import db
from application.rankings.models import Player, Ranking, RankingRecord
from . import Tournament


class TournamentPrize(db.Model):
    __tablename__ = 'TournamentPrize'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('Tournament.id'))
    position = db.Column(db.Integer)
    prize_money = db.Column(db.Float)
    ranking_points = db.Column(db.Integer)
    player_id = db.Column(db.Integer, db.ForeignKey('Player.id'))

    def __init__(self,
                 tournament: Tournament,
                 position: int,
                 prize_money: int = 0):
        self.tournament_id = tournament.id
        self.position = position
        self.prize_money = prize_money

    @property
    def player(self):
        if self.player_id:
            return Player.query.get(self.player_id)
        return None

    @staticmethod
    def distribute_prizes_for(tournament):
        prizes = TournamentPrize.query.filter_by(tournament_id=tournament.id).all()
        for prize in prizes:
            ranking = Ranking.query.filter_by(player_id=prize.player_id, list_id=tournament.ranking_list_id).first()
            rrecord = RankingRecord(ranking, prize.ranking_points)
            db.session.add(rrecord)
        db.session.commit()