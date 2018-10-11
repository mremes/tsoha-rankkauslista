from application import db
from typing import List
from sqlalchemy_utils.types.scalar_list import ScalarListType
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


class RankingList(db.Model):
    __tablename__ = 'RankingList'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genders = db.Column(ScalarListType(str))
    age_cap_hi = db.Column(db.Integer)
    age_cap_lo = db.Column(db.Integer)

    # transient
    players = None

    def __init__(self, name: str, genders: List[str], ach: int, acl: int):
        self.name = name
        self.genders = genders
        self.age_cap_hi = ach
        self.age_cap_lo = acl

    def populate_players(self):
        self.players = self._players()

    def _players(self):
        qry = """
        select player_id, ts, score
        from
        (
        select a.ranking_id ranking_id, a.timestamp ts, a.score score
        from RankingRecord a
        inner join
        (
        select id, max(timestamp) ts
        from RankingRecord
        group by id
        ) b
        on a.id = b.id and a.timestamp = b.ts
        ) a
        inner join
        (
        select id, player_id
        from Ranking
        where list_id = {}
        ) c
        on a.ranking_id = c.id
        """.format(self.id)

        results = db.engine.execute(qry)
        scores = {r[0]: (r[1], r[2]) for r in results}
        players = Player.query.filter(Player.id.in_(scores.keys())).all()

        for p in players:
            p.score = scores[p.id][1] or 0
            p.score_ts = scores[p.id][0]

        return players

    @staticmethod
    def get_suitable_ranking_lists(player):
        query = """
        SELECT * FROM RankingList
        WHERE genders LIKE '%%{gender}%%'
        AND {age} BETWEEN age_cap_lo AND age_cap_hi
        """.format(gender=player.gender,
                   age=datetime.now().year - player.dateofbirth.year)
        return RankingList.query.instances(db.engine.execute(query))

class Ranking(db.Model):
    __tablename__ = 'Ranking'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('Player.id'))
    list_id = db.Column(db.Integer, db.ForeignKey('RankingList.id'))

    def __init__(self, player: Player, ranking_list: RankingList):
        self.player_id = player.id
        self.list_id = ranking_list.id


class RankingRecord(db.Model):
    __tablename__ = 'RankingRecord'

    id = db.Column(db.Integer, primary_key=True)
    ranking_id = db.Column(db.Integer, db.ForeignKey('Ranking.id'))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    score = db.Column(db.Integer)

    def __init__(self, ranking: Ranking):
        self.ranking_id = ranking.id
        self.score = 0


class Tournament(db.Model):
    __tablename__ = 'Tournament'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String, nullable=False)
    ranking_list_id = db.Column(db.Integer, db.ForeignKey('RankingList.id'), nullable=False)

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

    def get_num_players(self):
        return len(TournamentPlayer.query.filter_by(tournament_id=self.id).all())


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


class TournamentPrize(db.Model):
    __tablename__ = 'TournamentPrize'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('Tournament.id'))
    position = db.Column(db.Integer)
    prize_money = db.Column(db.Float)

    def __init__(self,
                 tournament: Tournament,
                 position: int,
                 prize_money: int = 0):
        self.tournament_id = tournament.id
        self.position = position
        self.prize_money = prize_money


class Match(db.Model):
    __tablename__ = 'Match'

    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('TournamentPlayer.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('TournamentPlayer.id'))
    winner = db.Column(db.Integer, db.ForeignKey('TournamentPlayer.id'))

    def __init__(self,
                 tournament: Tournament,
                 player1: TournamentPlayer,
                 player2: TournamentPlayer):
        self.tournament_id = tournament.id
        self.player1_id = player1.id
        self.player2_id = player2.id


class TournamentMatch(db.Model):
    __tablename__ = 'TournamentMatch'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('Tournament.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('Match.id'))
    prize_id = db.Column(db.Integer, db.ForeignKey('TournamentPrize.id'))

    def __init__(self,
                 tournament: Tournament,
                 match: Match,
                 prize: TournamentPrize):
        self.tournament_id = tournament.id
        self.match_id = match.id
        self.prize_id = prize.id
