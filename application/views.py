from flask import render_template, jsonify
from application import app, db
from application.auth.models import User
from application.rankings.models import Player


@app.route('/')
def index():
    return render_template('index.html', players=Player.query.all())

# todo: endpoint turnauslistan luomiseen


@app.route('/create_list', methods=['GET'])
def create_list_give_player_names():
    # todo: filter players that are not in some other tournament
    session = db.session()
    players = [p.name for p in session.query(User).all()]
    return jsonify(players)
