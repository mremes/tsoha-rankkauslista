from application import db
from application.rankings.models import TournamentPlayer
from datetime import datetime


class Tournament(db.Model):
    __tablename__ = 'Tournament'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String, nullable=False)
    ranking_list_id = db.Column(db.Integer, db.ForeignKey('RankingList.id'), nullable=False)
    is_published = db.Column(db.Boolean)
    is_completed = db.Column(db.Boolean)

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
        self.is_completed = False
        self.is_published = False

    def get_num_players(self):
        return len(TournamentPlayer.query.filter_by(tournament_id=self.id).all())

    def set_completed(self):
        self.is_completed = True
        db.session.commit()
