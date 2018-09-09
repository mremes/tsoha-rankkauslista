from application import db


class BaseModel:
    @db.declared_attr
    def __tablename__(self):
        return self.__name__.lower()


class IdModel(BaseModel):
    id = db.Column(db.Integer, primary_key=True)


class Player(IdModel, db.Model):
    registered_ts = db.Column(db.Time)


class Association(IdModel, db.Model):
    pass

    
class RankingList(IdModel, db.Model):
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))


class Ranking(IdModel, db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    list_id = db.Column(db.Integer, db.ForeignKey('rankinglist.id'))


class RankingRecord(BaseModel, db.Model):
    ranking_id = db.Column(db.Integer, db.ForeignKey('ranking.id'))
    updated_ts = db.Column(db.Time)
    score = db.Column(db.Integer)

