from application import db
from datetime import datetime
from typing import List
from sqlalchemy_utils.types.scalar_list import ScalarListType


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    dateofbirth = db.Column(db.DateTime, nullable=False)
    placeofbirth = db.Column(db.String, nullable=False)
    registered_dt = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name: str,
                 gender: str,
                 dateofbirth: datetime,
                 placeofbirth: str):
        self.name = name
        self.gender = gender
        self.dateofbirth = dateofbirth
        self.placeofbirth = placeofbirth
        self.score = None
        self.score_ts = None

    @staticmethod
    def get_genders():
        return {'mies', 'nainen', 'muu'}


class Association(db.Model):
    __tablename__ = 'association'
    id = db.Column(db.Integer, primary_key=True)

    
class RankingList(db.Model):
    __tablename__ = 'rankinglist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genders = db.Column(ScalarListType(str))
    age_cap_hi = db.Column(db.Integer)
    age_cap_lo = db.Column(db.Integer)

    def __init__(self, name: str, genders: List[str], ach: int, acl: int):
        # noinspection PyTypeChecker
        self.name = name
        self.genders = genders
        self.age_cap_hi = ach
        self.age_cap_lo = acl


class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    list_id = db.Column(db.Integer, db.ForeignKey('rankinglist.id'))

    def __init__(self, player: Player, rankinglist: RankingList):
        self.player_id = player.id
        self.list_id = rankinglist.id


class RankingRecord(db.Model):
    __tablename__ = 'rankingrecord'

    id = db.Column(db.Integer, primary_key=True)
    ranking_id = db.Column(db.Integer, db.ForeignKey('ranking.id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    score = db.Column(db.Integer)

    def __init__(self, ranking: Ranking):
        self.ranking_id = ranking.id
        self.score = 0
