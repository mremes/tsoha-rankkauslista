from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required
from application import app, db
from application.rankings.models import Player, RankingList, Ranking, RankingRecord
from application.forms import PlayerForm, RankingListForm
import datetime as dt
import application.utils as utils


@app.route('/register_player', methods=['GET', 'POST'])
def register_player():
    form = PlayerForm(request.form)
    if form.validate_on_submit():
        player = Player(form.name.data, form.gender.data, form.dob.data, form.pob.data)
        db.session().add(player)
        db.session().commit()
        flash(u'Onnistuneesti lisätty pelaaja: %s' % player.name)
        return redirect(url_for('index'))
    return render_template('register_player.html', form=form)


@app.route('/players/<int:playerid>')
def get_player_info(playerid):
    player_data = Player.query.get(playerid)

    if player_data:
        return render_template('player_info.html', data=[player_data])
    else:
        flash('Pelaajaa tunnuksella %s ei ole olemassa.' % playerid)
        return redirect(utils.get_next_url())


@app.route('/players/<playerid>/edit', methods=['GET', 'POST'])
@login_required
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
        return render_template('player_info.html', data=[player])

    return render_template('edit_player.html', form=form)


@app.route('/players/<playerid>/add_to_list', methods=['GET'])
#@login_required
def add_to_ranking_list(playerid):
    listid = request.args.get('listid')
    player = Player.query.get(playerid)
    if not player:
        flash('Pelaajaa tunnuksella %s ei ole olemassa.' % playerid)
        return redirect(utils.get_next_url())
    if listid:
        rlist = RankingList.query.get(listid)
        if not listid:
            # todo: fix this
            return 'Listaa ei ole olemassa', 404
        ranking = Ranking(player, rlist)
        db.session().add(ranking)
        db.session().commit()
        rankingrecord = RankingRecord(ranking)
        rankingrecord.score = 0
        db.session().add(rankingrecord)
        db.session().commit()
        flash('Pelaaja %s onnistuneesti lisätty listalle %s' % (playerid, listid))
        return redirect(utils.get_next_url())

    player = Player.query.get(playerid)
    query = """
    SELECT * FROM RankingList
    WHERE genders LIKE '%%{gender}%%'
    AND {age} BETWEEN age_cap_lo AND age_cap_hi
    """.format(gender=player.gender,
               age=dt.datetime.now().year - player.dateofbirth.year)
    lists = RankingList.query.instances(db.engine.execute(query))
    return render_template('add_player_to_ranking_list.html', data=[player], lists=lists)


@app.route('/players/<playerid>/retire', methods=['GET'])
@login_required
def retire_player(playerid):
    player_data = Player.query.get(playerid)
    if not player_data:
        flash('Pelaajaa tunnuksella %s ei ole olemassa.' % playerid)
        return redirect(utils.get_next_url())
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

    qry = """
    select player_id, timestamp ts, score
    from
    (
    select a.ranking_id ranking_id, a.timestamp timestamp, a.score score
    from rankingrecord a
    inner join
    (
    select id, max(timestamp) timestamp
    from rankingrecord
    group by id
    ) b
    on a.id = b.id and a.timestamp = b.timestamp
    ) a
    inner join
    (
    select id, player_id
    from ranking
    where list_id = {}
    ) c
    on a.ranking_id = c.id
    """.format(ranking_list_id)

    results = db.engine.execute(qry)
    scores = {r[0]: (r[1], r[2]) for r in results}
    players = Player.query.filter(Player.id.in_(scores.keys())).all()

    for p in players:
        p.score = scores[p.id][1] or 0
        p.score_ts = scores[p.id][0]
        print(p.score)

    return render_template('ranking_list_info.html', data=[rlist], players=players)


@app.route('/create_ranking_list', methods=['GET', 'POST'])
@login_required
def create_ranking_list():
    form = RankingListForm(request.form)
    if form.validate_on_submit():
        gender_filter = form.gender_filter.data
        # quick and dirty hack; make this part of the responsible class
        assert gender_filter in ['mies', 'nainen', 'mikä tahansa']
        genders = []
        if gender_filter == 'mies':
            genders = ['mies']
        elif gender_filter == 'nainen':
            genders = ['nainen']
        elif gender_filter == 'mikä tahansa':
            genders = ['mies', 'nainen', 'muu']
        assert genders
        rankinglist = RankingList(form.name.data, genders, form.age_cap_hi.data, form.age_cap_lo.data)
        db.session().add(rankinglist)
        db.session().commit()
        flash(u'Onnistuneesti luotu lista: %s' % rankinglist.name)
        return redirect(url_for('index'))
    return render_template('create_ranking_list.html', form=form)
