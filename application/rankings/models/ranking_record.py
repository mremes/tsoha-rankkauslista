from application import db
from . import Ranking


class RankingRecord(db.Model):
    __tablename__ = 'RankingRecord'

    id = db.Column(db.Integer, primary_key=True)
    ranking_id = db.Column(db.Integer, db.ForeignKey('Ranking.id'))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    score = db.Column(db.Integer)

    def __init__(self, ranking: Ranking, score: int=0):
        self.ranking_id = ranking.id
        self.score = 0
        latest = RankingRecord.query.filter_by(ranking_id=ranking.id).order_by(RankingRecord.timestamp.desc()).first()
        if latest:
            self.score += latest.score
        self.score += score
