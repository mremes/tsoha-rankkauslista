from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required
from application import app, db
from application.rankings.models import Player, RankingList, Ranking, \
    RankingRecord, Tournament
from application.forms import PlayerForm, RankingListForm, TournamentInfoForm, \
    TournamentPlayersForm, TournamentLayoutForm, TournamentPrizesForm
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
# @login_required
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
    return render_template('add_player_to_ranking_list.html',
                           data=[player],
                           lists=lists)


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

    rlist.populate_players()
    return render_template('ranking_list_info.html', data=[rlist])


@app.route('/create_ranking_list', methods=['GET', 'POST'])
@login_required
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

    return render_template('create_ranking_list.html', form=form)


@app.route('/tournament/create', methods=['GET', 'POST'])
def create_tournament():
    data = {'progress': 0,
            'status_text': 'Vaihe 1: Anna turnauksen perustiedot'}
    form = TournamentInfoForm()

    if form.validate_on_submit():
        tournament = form.get_tournament_object()
        db.session().add(tournament)
        db.session().commit()

        return redirect(url_for('select_num_players_for_tournament',
                                tournament_id=tournament.id))

    rlist_choices = [(rlist.id, rlist.name) for rlist in RankingList.query.all()]
    form.ranking_list.choices = rlist_choices
    form.process()

    return render_template('create_tournament_1.html', data=data, form=form)


@app.route('/tournament/create/players', methods=['GET', 'POST'])
def select_num_players_for_tournament():
    tournament_id = request.args.get('tournament_id')
    data = {'progress': 25,
            'status_text': 'Vaihe 2: Valitse turnaukseen osallistuvien pelaajien lukumäärä'}
    tournament_players_form = TournamentPlayersForm(tournament_id)

    if tournament_players_form.validate_on_submit():
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            flash('Turnausta ei löydy.')
            return redirect(url_for('index'))
        num_players = tournament_players_form.num_players.data
        flash('%s pelaajaa.' % num_players)
        flash('Turnaus %s' % tournament.id)
        return redirect(url_for('set_players_for_tournament',
                                tournament_id=tournament_id,
                                num_players=num_players))

    return render_template('create_tournament_2.html',
                           data=data,
                           form=tournament_players_form,
                           tournament_id=tournament_id)


@app.route('/tournament/create/set_players', methods=['GET', 'POST'])
def set_players_for_tournament():
    tournament_id = request.args.get('tournament_id')
    tournament = Tournament.query.get(tournament_id)
    data = {'progress': 50,
            'post_url': 'set_players_for_tournament',
            'status_text': 'Vaihe 3: Asettele vapaat pelaajat turnaukseen'}

    form = TournamentLayoutForm()

    if not form.validate_on_submit():
        num_players = int(request.args.get('num_players'))
        tournament = Tournament.query.get(tournament_id)
        rlist = RankingList.query.get(tournament.ranking_list_id)
        rlist.populate_players()
        TournamentLayoutForm.update_form_fields(num_players, rlist)
        form = TournamentLayoutForm()
    else:
        matches = form.create_matches(tournament)
        flash('Luotu %d ottelua.' % len(matches))
        return redirect(url_for('set_prizes_for_tournament',
                                tournament_id=tournament_id))

    return render_template('dynamic_attributes_form.html',
                           tournament_id=tournament_id,
                           data=data,
                           form=form)


@app.route('/tournament/create/set_prizes', methods=['GET', 'POST'])
def set_prizes_for_tournament():
    data = {'progress': 75,
            'post_url': 'set_prizes_for_tournament',
            'status_text': 'Vaihe 4: Anna turnauksen palkintojen tiedot'}
    tournament_id = request.args.get('tournament_id')
    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei löydy.')
        return redirect(url_for('index'))

    form = TournamentPrizesForm()
    if not form.validate_on_submit():
        num_players = tournament.get_num_players()
        for i in range(20):
            print(num_players)
        TournamentPrizesForm.update_form_fields(num_players)
        form = TournamentPrizesForm()
    else:
        prizes = form.create_prizes(tournament)
        flash('Luotu %d palkintoa.' % len(prizes))
        return redirect(url_for('tournament_ready'))

    return render_template('dynamic_attributes_form.html',
                           tournament_id=tournament_id,
                           data=data,
                           form=form)


@app.route('/tournament/create/ready', methods=['GET'])
def tournament_ready():
    tournament_id = request.args.get('tournament_id')
    data = {'progress': 100}
    return render_template('tournament_ready.html', data=data)
