from application import db
from datetime import datetime

class Tournament(db.Model):
    __tablename__ = 'Tournament'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String, nullable=False)
    ranking_list_id = db.Column(
        db.Integer, db.ForeignKey('RankingList.id'), nullable=False)

    # transient
    num_players = None

    def __init__(self,
                 name: str,
                 venue: str,
                 date: datetime,
                 ranking_list_id: int):
        self.name = name
        self.venue = venue
        self.date = date
        self.ranking_list_id = ranking_list_id
