from flask import flash, redirect, url_for, render_template, request
from flask_login import current_user
from application import app, db
from application.rankings.models import RankingList, Ranking, RankingRecord
from application.players.models import Player
from application.players.forms import PlayerForm
import application.utils as utils
from application import login_required


@app.route('/players/register', methods=['GET', 'POST'])
@login_required(["PLAYER", "ADMIN"])
def register_player():
    form = PlayerForm(request.form)
    if form.validate_on_submit():
        player = Player(form.name.data, form.gender.data,
                        form.dob.data, form.pob.data, current_user)
        db.session().add(player)
        db.session().commit()
        flash(u'Onnistuneesti lisätty pelaaja: %s' % player.name)
        return redirect(url_for('index'))
    return render_template('players/register_player.html', form=form)


@app.route('/players/<int:playerid>')
def get_player_info(playerid):
    player_data = Player.query.get(playerid)

    if player_data:
        rlists = RankingList.query.filter(
            RankingList.id.in_([r.list_id for r in Ranking.query.filter_by(player_id=player_data.id)]))
        return render_template('players/player_info.html', data=[player_data], rlists=rlists)
    else:
        flash('Pelaajaa tunnuksella %s ei ole olemassa.' % playerid)
        return redirect(utils.get_next_url())


@app.route('/players/<int:playerid>/edit', methods=['GET', 'POST'])
@login_required(["PLAYER", "ADMIN"])
def edit_player(playerid):
    player = Player.query.get(playerid)

    if not player:
        flash('Pelaajaa tunnuksella %s ei ole olemassa.' % playerid)
        return redirect(utils.get_next_url())

    form = PlayerForm(player=player)

    if form.validate_on_submit():
        player = db.session.query(Player).get(playerid)
        player.name = form.name.data
        player.gender = form.gender.data
        player.dateofbirth = form.dob.data
        player.placeofbirth = form.pob.data
        db.session.commit()
        flash('Onnistuneesti muokattiin pelaajaa %s' % playerid)
        return render_template('players/player_info.html', data=[player])

    return render_template('players/edit_player.html', form=form)


@app.route('/players/<int:playerid>/retire', methods=['GET'])
@login_required(["PLAYER", "ADMIN"])
def retire_player(playerid):
    player_data = Player.query.get(playerid)

    if not player_data:
        flash('Pelaajaa tunnuksella %s ei ole olemassa.' % playerid)
        return redirect(utils.get_next_url())

    rankings = Ranking.query.filter_by(player_id=player_data.id).all()
    for ranking in rankings:
        RankingRecord.query.filter_by(ranking_id=ranking.id).delete()
    Ranking.query.filter_by(player_id=player_data.id).delete()
    db.session().delete(player_data)
    db.session.commit()

    flash('Onnistuneesti poistettiin pelaaja %s.' % player_data.name)
    return redirect(url_for('index'))
