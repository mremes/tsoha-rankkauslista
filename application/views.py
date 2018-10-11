from flask import render_template, jsonify
from application import app, db
from application.auth.models import User
from application.rankings.models import Player, RankingList, Tournament


@app.route('/')
def index():
    lists = RankingList.query.all()
    for l in lists:
        l.populate_players()
    tournaments = Tournament.query.all()
    for t in tournaments:
        t.num_players = t.get_num_players()
    return render_template('index.html',
                           players=Player.query.all(),
                           rankings=lists,
                           tournaments=tournaments)

# todo: endpoint turnauslistan luomiseen


@app.route('/create_list', methods=['GET'])
def create_list_give_player_names():
    # todo: filter players that are not in some other tournament
    session = db.session()
    players = [p.name for p in session.query(User).all()]
    return jsonify(players)
