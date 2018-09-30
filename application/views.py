from flask import render_template, jsonify
from application import app, db
from application.auth.models import User
from application.rankings.models import Player, RankingList, Ranking


@app.route('/')
def index():
    lists = RankingList.query.all()
    query="""
    SELECT list_id, COUNT(DISTINCT player_id) FROM Ranking
    GROUP BY list_id
    """
    results = db.engine.execute(query)
    num_players = {r[0]: r[1] for r in results}
    return render_template('index.html', players=Player.query.all(), rankings=lists, num_players=num_players)

# todo: endpoint turnauslistan luomiseen


@app.route('/create_list', methods=['GET'])
def create_list_give_player_names():
    # todo: filter players that are not in some other tournament
    session = db.session()
    players = [p.name for p in session.query(User).all()]
    return jsonify(players)
