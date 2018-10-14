from application import db
from datetime import datetime


class Player(db.Model):
    __tablename__ = 'Player'

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
