from application import db
from . import Tournament, Player


class TournamentPlayer(db.Model):
    __tablename__ = 'TournamentPlayer'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('Tournament.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('Player.id'))
    position = db.Column(db.Integer, server_default='-1')

    def __init__(self,
                 tournament: Tournament,
                 player: Player):
        self.tournament_id = tournament.id
        self.player_id = player.id

    def update_position(self, position: int):
        self.position = position

    @staticmethod
    def get_num_players_in_tournament(tournament):
        return len(TournamentPlayer.query.filter_by(tournament_id=tournament.id).all())
