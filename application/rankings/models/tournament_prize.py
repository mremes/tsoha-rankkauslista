from application import db
from . import Tournament


class TournamentPrize(db.Model):
    __tablename__ = 'TournamentPrize'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('Tournament.id'))
    position = db.Column(db.Integer)
    prize_money = db.Column(db.Float)

    def __init__(self,
                 tournament: Tournament,
                 position: int,
                 prize_money: int = 0):
        self.tournament_id = tournament.id
        self.position = position
        self.prize_money = prize_money
