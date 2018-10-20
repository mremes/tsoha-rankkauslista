from application import db
from . import Player, RankingList


class Ranking(db.Model):
    __tablename__ = 'Ranking'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('Player.id'))
    list_id = db.Column(db.Integer, db.ForeignKey('RankingList.id'))

    def __init__(self, player: Player, ranking_list: RankingList):
        self.player_id = player.id
        self.list_id = ranking_list.id