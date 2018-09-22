from flask import flash, redirect, url_for, render_template, request, abort
from flask_login import login_required
from application import app, db
from application.auth.models import User
from application.rankings.models import Player
from application.forms import PlayerForm

import application.utils as utils


@app.route("/register_player", methods=["GET", "POST"])
def register_player():
    form = PlayerForm(request.form)
    if form.validate_on_submit():
        player = Player(form.name.data, form.gender.data, form.dob.data, form.pob.data)
        db.session().add(player)
        db.session().commit()
        flash(u'Onnistuneesti lisätty pelaaja: %s' % player.name)
        return redirect(url_for('index'))
    return render_template('register_player.html', form=form)


@app.route("/players/<int:playerid>")
def get_player_info(playerid):
    player_data = Player.query.get(playerid)

    if player_data:
        return render_template("player_info.html", data=[player_data])
    else:
        flash('Player with id %s does not exists.' % playerid)
        return redirect(utils.get_next_url())


@login_required
@app.route("/players/<playerid>/edit", methods=["GET", "POST"])
def edit_player(playerid):
    player = Player.query.get(playerid)

    if not player:
        flash("Player with id %s does not exist" % playerid)
        return redirect(utils.get_next_url())

    form = PlayerForm(player=player)

    if form.validate_on_submit():
        player = db.session.query(Player).get(playerid)
        player.name = form.name.data
        player.gender = form.gender.data
        player.dateofbirth = form.dob.data
        player.placeofbirth = form.pob.data
        db.session.commit()
        flash("Onnistuneesti muokattiin pelaajaa %s" % playerid)
        return render_template("player_info.html", data=[player])

    return render_template("edit_player.html", form=form)

@login_required
@app.route("/players/<playerid>/retire", methods=["GET"])
def retire_player(playerid):
    player_data = Player.query.get(playerid)
    if not player_data:
        flash("Player with id not found")
        return redirect(utils.get_next_url())
    db.session().delete(player_data)
    db.session.commit()
    flash("Player %s successfully retired" % player_data.name)
    return redirect(url_for('index'))
