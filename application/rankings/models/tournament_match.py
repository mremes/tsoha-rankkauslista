from application import db
from . import Tournament, Match, TournamentPrize


class TournamentMatch(db.Model):
    __tablename__ = 'TournamentMatch'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('Tournament.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('Match.id'))
    prize_id = db.Column(db.Integer, db.ForeignKey('TournamentPrize.id'))

    def __init__(self,
                 tournament: Tournament,
                 match: Match,
                 prize: TournamentPrize):
        self.tournament_id = tournament.id
        self.match_id = match.id
        self.prize_id = prize.id
