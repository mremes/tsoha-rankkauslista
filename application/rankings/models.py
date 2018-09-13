from application import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    registered_dt = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name: str):
        self.name = name

    @property
    def score(self):
        session = db.session()
        ranking = session.query(Ranking).filter_by(player_id=self.id).first()
        if not ranking:
            return -1


class Association(db.Model):
    __tablename__ = 'association'
    id = db.Column(db.Integer, primary_key=True)

    
class RankingList(db.Model):
    __tablename__ = 'rankinglist'

    id = db.Column(db.Integer, primary_key=True)
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    def __init__(self, assoc: Association):
        self.assoc_id = assoc.id


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