from application import db
from application.auth.models import User
from datetime import datetime


class Player(db.Model):
    __tablename__ = 'Player'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    dateofbirth = db.Column(db.DateTime, nullable=False)
    placeofbirth = db.Column(db.String, nullable=False)
    registered_dt = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name: str,
                 gender: str,
                 dateofbirth: datetime,
                 placeofbirth: str,
                 created_by: User):
        self.name = name
        self.gender = gender
        self.dateofbirth = dateofbirth
        self.placeofbirth = placeofbirth
        self.created_by = created_by.id

    @staticmethod
    def get_genders():
        return {'mies', 'nainen', 'muu'}

    @staticmethod
    def get_aggregate_summary():
        qry = """
        SELECT 
            id,
            name,
            SUM(list_count) list_count,
            SUM(score) score
        FROM 
            "Player" a
        LEFT JOIN
            (
            SELECT 
                player_id,
                COUNT(DISTINCT list_id) list_count
            FROM 
                "Ranking"
            GROUP BY 
                player_id
            ) b
        ON 
            a.id = b.player_id
        LEFT JOIN
            (
            SELECT 
                c.player_id player_id,
                score
            FROM
               "RankingRecord" a
            INNER JOIN
                (
                SELECT 
                    ranking_id,
                    MAX(timestamp) maxts
                FROM 
                    "RankingRecord"
                GROUP BY 
                    ranking_id 
                ) b
            ON 
              a.ranking_id = b.ranking_id AND a.timestamp = b.maxts
            LEFT JOIN 
              "Ranking" c
            ON a.ranking_id = c.id
            ) c
        ON 
            a.id = c.player_id
        GROUP BY
            id,
            name
        """

        res = db.engine.execute(qry)
        result = []
        for row in res:
            r = {'id': row[0], 'name': row[1], 'num_lists': row[2], 'score': row[3]}
            result.append(r)
        return result
