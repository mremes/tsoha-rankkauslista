from application import db
from . import Ranking


class RankingRecord(db.Model):
    __tablename__ = 'RankingRecord'

    id = db.Column(db.Integer, primary_key=True)
    ranking_id = db.Column(db.Integer, db.ForeignKey('Ranking.id'))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    score = db.Column(db.Integer)

    def __init__(self, ranking: Ranking):
        self.ranking_id = ranking.id
        self.score = 0
