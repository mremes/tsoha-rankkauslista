from application import db
from application.rankings.models import Tournament, TournamentPlayer


class Match(db.Model):
    __tablename__ = 'Match'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('Tournament.id'))
    player1_id = db.Column(db.Integer, db.ForeignKey('TournamentPlayer.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('TournamentPlayer.id'))
    winner = db.Column(db.Integer, db.ForeignKey('TournamentPlayer.id'))

    def __init__(self,
                 tournament: Tournament,
                 player1: TournamentPlayer,
                 player2: TournamentPlayer):
        self.tournament_id = tournament.id
        self.player1_id = player1.id
        self.player2_id = player2.id
