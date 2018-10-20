from flask import render_template
from application import app
from application.rankings.models import Player, RankingList, Tournament, TournamentPlayer


@app.route('/')
def index():
    lists = RankingList.query.all()
    for l in lists:
        l.populate_players()
    tournaments = Tournament.query.filter_by(is_published=True).all()
    for t in tournaments:
        t.num_players = t.get_num_players()
    player_data = Player.get_aggregate_summary()
    print(player_data)
    return render_template('index.html',
                           player_data=player_data,
                           rankings=lists,
                           tournaments=tournaments)
