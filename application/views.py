from flask import render_template
from application import app
from application.rankings.models import Player, RankingList, Tournament, TournamentPlayer


@app.route('/')
def index():
    lists = RankingList.query.all()
    for l in lists:
        l.populate_players()
    tournaments = Tournament.query.all()
    for t in tournaments:
        t.num_players = TournamentPlayer.get_num_players_in_tournament(t)

    return render_template('index.html',
                           players=Player.query.all(),
                           rankings=lists,
                           tournaments=tournaments)
