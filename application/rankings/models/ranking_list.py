from application import db
from typing import List
from sqlalchemy_utils.types.scalar_list import ScalarListType
from sqlalchemy import text
from datetime import datetime

from . import Player


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
        from "RankingRecord" a
        inner join
        (
        select id, max(timestamp) ts
        from "RankingRecord"
        group by id
        ) b
        on a.id = b.id and a.timestamp = b.ts
        ) a
        inner join
        (
        select id, player_id
        from "Ranking"
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
        query = text("""
        SELECT * FROM "RankingList"
        WHERE genders LIKE :gender
        AND :age BETWEEN age_cap_lo AND age_cap_hi
        AND id NOT IN
        (
        SELECT list_id FROM "Ranking" WHERE player_id = :user_id
        )
        """).params(gender="%{}%".format(player.gender),
                    age=datetime.now().year - player.dateofbirth.year,
                    user_id=player.id)
        return list(RankingList.query.instances(db.engine.execute(query)))
