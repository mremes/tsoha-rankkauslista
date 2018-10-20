from flask import flash, redirect, url_for, render_template, request
from flask_login import current_user
from application import app, db
from application.rankings import TournamentPrize, Match
from application.rankings.models import Player, RankingList, Ranking, \
    RankingRecord, Tournament, TournamentPlayer
from application.forms import PlayerForm, RankingListForm, TournamentInfoForm, \
    TournamentPlayersForm, TournamentLayoutForm, TournamentPrizesForm
import application.utils as utils
from application import login_required


@app.route('/register_player', methods=['GET', 'POST'])
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
    return render_template('register_player.html', form=form)


@app.route('/players/<int:playerid>')
def get_player_info(playerid):
    player_data = Player.query.get(playerid)

    if player_data:
        rlists = RankingList.query.filter(RankingList.id.in_([r.list_id for r in Ranking.query.filter_by(player_id=player_data.id)]))
        return render_template('player_info.html', data=[player_data], rlists=rlists)
    else:
        flash('Pelaajaa tunnuksella %s ei ole olemassa.' % playerid)
        return redirect(utils.get_next_url())


@app.route('/players/<playerid>/edit', methods=['GET', 'POST'])
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
        return render_template('player_info.html', data=[player])

    return render_template('edit_player.html', form=form)


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
    return render_template('add_player_to_ranking_list.html',
                           data=[player],
                           lists=lists)


@app.route('/players/<playerid>/retire', methods=['GET'])
@login_required(["PLAYER", "ADMIN"])
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

    return render_template('create_ranking_list.html', form=form)


@app.route('/tournament/create', methods=['GET', 'POST'])
@login_required(["TOURNAMENT", "ADMIN"])
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

    rlist_choices = [(rlist.id, rlist.name)
                     for rlist in RankingList.query.all()]
    form.ranking_list.choices = rlist_choices
    form.process()

    return render_template('create_tournament_1.html', data=data, form=form)


@app.route('/tournament/create/players', methods=['GET', 'POST'])
@login_required(["TOURNAMENT", "ADMIN"])
def select_num_players_for_tournament():
    tournament_id = request.args.get('tournament_id')
    if not tournament_id:
        flash('Tournament_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        flash('Turnausta ei ole olemassa.')
        return redirect(utils.get_next_url())

    data = {'progress': 25,
            'status_text': 'Vaihe 2: Valitse turnaukseen osallistuvien pelaajien lukumäärä',
            'button_label': 'Seuraava'}
    tournament_players_form = TournamentPlayersForm(tournament)

    if tournament_players_form.validate_on_submit():
        num_players = tournament_players_form.num_players.data
        return redirect(url_for('set_players_for_tournament',
                                tournament_id=tournament_id,
                                num_players=num_players))

    return render_template('create_tournament_2.html',
                           data=data,
                           form=tournament_players_form,
                           tournament_id=tournament_id)


@app.route('/tournament/create/set_players', methods=['GET', 'POST'])
@login_required(["TOURNAMENT", "ADMIN"])
def set_players_for_tournament():
    tournament_id = request.args.get('tournament_id')
    num_players = int(request.args.get('num_players'))
    if not tournament_id:
        flash('Turnaus_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        flash('Turnaus ei ole olemassa')
        return redirect(utils.get_next_url())

    data = {'progress': 50,
            'post_url': 'set_players_for_tournament',
            'status_text': 'Vaihe 3: Asettele vapaat pelaajat turnaukseen',
            'button_label': 'Seuraava'}

    form = TournamentLayoutForm(tournament)

    if not form.validate_on_submit():
        form.update_layout_fields()
        form = TournamentLayoutForm(tournament)
    else:
        matches = form.create_matches()
        flash('Luotu %d ottelua.' % len(matches))
        return redirect(url_for('set_prizes_for_tournament',
                                tournament_id=tournament_id))

    return render_template('dynamic_attributes_form.html',
                           tournament_id=tournament_id,
                           num_players=num_players,
                           data=data,
                           form=form)


@app.route('/tournament/create/set_prizes', methods=['GET', 'POST'])
@login_required(["TOURNAMENT", "ADMIN"])
def set_prizes_for_tournament():
    data = {'progress': 75,
            'post_url': 'set_prizes_for_tournament',
            'status_text': 'Vaihe 4: Anna turnauksen palkintojen tiedot',
            'button_label': 'Valmis'}
    tournament_id = request.args.get('tournament_id')
    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei löydy.')
        return redirect(utils.get_next_url())

    form = TournamentPrizesForm(tournament)
    if not form.validate_on_submit():
        form.create_prizes_fields()
        form = TournamentPrizesForm(tournament)
    else:
        prizes = form.create_prizes()
        flash('Luotu %d palkintoa.' % len(prizes))
        return redirect(url_for('tournament_ready', tournament_id=tournament_id))

    return render_template('dynamic_attributes_form.html',
                           tournament_id=tournament_id,
                           data=data,
                           form=form)


@app.route('/tournament/create/ready', methods=['GET'])
@login_required(["TOURNAMENT", "ADMIN"])
def tournament_ready():
    tournament_id = request.args.get('tournament_id')
    if not tournament_id:
        flash('Turnaus_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei ole olemassa.')
        return redirect(utils.get_next_url())

    tournament.is_published = True
    db.session.commit()

    data = {'progress': 100}

    return render_template('tournament_ready.html', data=data)


@app.route('/tournament/<tournament_id>', methods=['GET'])
def get_tournament_info(tournament_id):
    if not tournament_id:
        flash('Turnaus_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei ole olemassa.')
        return redirect(utils.get_next_url())

    tournament_players = TournamentPlayer.query.filter_by(tournament_id=tournament_id).all()
    players = Player.query.filter(Player.id.in_([p.player_id for p in tournament_players]))
    ranking_list = RankingList.query.get(tournament.ranking_list_id)
    tournament_info = [('Ajankohta', tournament.date),
                       ('Kisapaikka', tournament.venue),
                       ('Ranking-listan nimi', ranking_list.name),
                       ('Pelaajien lukumäärä', len(tournament_players))]

    tournament_matches = Match.query.filter_by(tournament_id=tournament_id).all()

    matches_info = []
    for match in tournament_matches:
        match_info = {'player1': Player.query.get(TournamentPlayer.query.get(match.player1_id).player_id).name,
                      'player2': Player.query.get(TournamentPlayer.query.get(match.player2_id).player_id).name}
        matches_info.append(match_info)

    return render_template('tournament.html',
                           tournament=tournament,
                           tournament_prizes=TournamentPrize.query.filter_by(tournament_id=tournament.id).all(),
                           name=tournament.name,
                           tournament_info=tournament_info,
                           matches_info=matches_info,
                           players_info=players)


@app.route('/tournament/<tournament_id>/set_results', methods=['GET', 'POST'])
@login_required(["TOURNAMENT", "ADMIN"])
def tournament_set_results(tournament_id):
    if not tournament_id:
        flash('Turnaus_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei ole olemassa.')
        return redirect(utils.get_next_url())

    form = TournamentLayoutForm(tournament)

    if not form.validate_on_submit():
        form.update_standings_fields()
        form = TournamentLayoutForm(tournament)
    else:
        form.update_prizes()
        flash('Sijoitukset päivitetty')
        return redirect(url_for('get_tournament_info', tournament_id=tournament_id))

    data = {'button_label': 'Vahvista sijoitukset',
            'status_text': 'Syötä pelaajien sijoitukset',
            'post_url': 'tournament_set_results'}

    return render_template('dynamic_attributes_form.html',
                           tournament_id=tournament_id,
                           data=data,
                           form=form)


@app.route('/tournament/<tournament_id>/set_ranking_points', methods=["GET", "POST"])
@login_required(["ADMIN"])
def tournament_set_ranking_points(tournament_id):
    if not tournament_id:
        flash('Turnaus_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei ole olemassa.')
        return redirect(utils.get_next_url())

    form = TournamentPrizesForm(tournament)
    if not form.validate_on_submit():
        form.create_ranking_points_fields()
        form = TournamentPrizesForm(tournament)
    else:
        form.update_ranking_points()
        flash('Ranking-pisteet päivitetty.')
        return redirect(url_for('get_tournament_info', tournament_id=tournament_id))

    data = {'button_label': 'Vahvista pisteet',
            'status_text': 'Syötä sijoituksista saatavat ranking-pisteet',
            'post_url': 'tournament_set_ranking_points'}
    return render_template('dynamic_attributes_form.html',
                           tournament_id=tournament_id,
                           data=data,
                           form=form)


@app.route('/tournament/<tournament_id>/complete', methods=["POST"])
@login_required(["TOURNAMENT", "ADMIN"])
def complete_tournament(tournament_id):
    if not tournament_id:
        flash('Turnaus_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei ole olemassa.')
        return redirect(utils.get_next_url())

    tournament.set_completed()
    TournamentPrize.distribute_prizes_for(tournament)
    return redirect(url_for('get_tournament_info', tournament_id=tournament_id))


@app.route('/tournament/<tournament_id>/delete', methods=["POST"])
@login_required(["TOURNAMENT", "ADMIN"])
def delete_tournament(tournament_id):
    if not tournament_id:
        flash('Turnaus_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei ole olemassa.')
        return redirect(utils.get_next_url())

    db.session.delete(TournamentPrize.query.filter_by(tournament_id=tournament_id))
    db.session.delete(TournamentPlayer.query.filter_by(tournament_id=tournament_id))
    db.session.delete(tournament)
    db.session.commit()


@app.route('/tournament/<tournament_id>/edit', methods=["GET", "POST"])
@login_required(["TOURNAMENT", "ADMIN"])
def tournament_edit_details(tournament_id):
    if not tournament_id:
        flash('Turnaus_id ei voi olla tyhjä.')
        return redirect(utils.get_next_url())

    tournament = Tournament.query.get(tournament_id)

    if not tournament:
        flash('Turnausta ei ole olemassa.')
        return redirect(utils.get_next_url())

    form = TournamentInfoForm(tournament=tournament)

    if form.validate_on_submit():
        tournament = Tournament.query.get(tournament_id)
        tournament.name = form.name.data
        tournament.venue = form.venue.data
        tournament.date = form.date.data
        db.session.commit()
        flash('Onnistuneesti muokattiin turnausta %s' % tournament_id)
        return redirect(url_for('get_tournament_info', tournament_id=tournament_id))

    return render_template('edit_tournament.html', form=form, tournament_id=tournament_id)
