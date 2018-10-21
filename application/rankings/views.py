from flask import flash, redirect, url_for, render_template, request
from application import app, db
from application.players.models import Player
from application.rankings.models import RankingList, Ranking, RankingRecord
from application.rankings.forms import RankingListForm
import application.utils as utils
from application import login_required


@app.route('/players/<playerid>/add_to_list', methods=['GET'])
@login_required(["PLAYER", "ADMIN"])
def add_to_ranking_list(playerid):
    listid = request.args.get('listid')
    player = Player.query.get(playerid)

    if not player:
        flash('Pelaajaa tunnuksella %s ei ole olemassa.' % playerid)
        return redirect(utils.get_next_url())

    if listid:
        rlist = RankingList.query.get(listid)

        ranking = Ranking(player, rlist)
        db.session().add(ranking)
        db.session.commit()

        rankingrecord = RankingRecord(ranking)
        db.session().add(rankingrecord)
        db.session().commit()

        flash('Pelaaja %s onnistuneesti lisätty listalle %s'
              % (playerid, listid))
        return redirect(utils.get_next_url())

    player = Player.query.get(playerid)
    lists = RankingList.get_suitable_ranking_lists(player)
    return render_template('players/add_player_to_ranking_list.html',
                           data=[player],
                           lists=lists)


@app.route('/players/<playerid>/retire', methods=['GET'])
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


@app.route('/lists/<ranking_list_id>', methods=['GET'])
def get_list_info(ranking_list_id):
    rlist = RankingList.query.get(ranking_list_id)

    if not rlist:
        flash('Listaa tunnuksella %s ei ole olemassa' % ranking_list_id)
        return redirect(utils.get_next_url())

    rlist.populate_players()
    return render_template('rankings/ranking_list_info.html', data=[rlist])


@app.route('/create_ranking_list', methods=['GET', 'POST'])
@login_required(["ADMIN"])
def create_ranking_list():
    form = RankingListForm(request.form)

    if form.validate_on_submit():
        rankinglist = RankingList(form.name.data,
                                  form.genders,
                                  form.age_cap_hi.data,
                                  form.age_cap_lo.data)
        db.session().add(rankinglist)
        db.session().commit()
        flash(u'Onnistuneesti luotu lista: %s' % rankinglist.name)
        return redirect(url_for('index'))

    return render_template('rankings/create_ranking_list.html', form=form)
