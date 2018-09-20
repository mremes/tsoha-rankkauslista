from flask import flash, redirect, url_for, render_template, request, jsonify, abort
from application import app, db
from application.auth.models import User
from application.rankings.models import Player
from application.forms import LoginForm, RegisterForm, PlayerForm
import application.auth.login as app_login
from urllib.parse import urlparse, urljoin


@app.route("/")
def index():
    return render_template('index.html', players=Player.query.all())


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(form.name.data, form.username.data, form.password.data)
        db.session().add(user)
        db.session().commit()
        flash(u'Onnistuneesti rekisteröitynyt käyttäjä: %s' % user.username)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


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


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.user.username)
        next = request.args.get('next')
        app_login.login_user(form.user)
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)


@app.route("/logout", methods=["GET"])
def logout():
    app_login.logout_user()
    flash(u'Logged out user.')
    return redirect(url_for('index'))


@app.route("/players/<int:userid>")
def get_player_info(userid):
    template_name = 'user_info.html'
    session = db.session()
    player_data = session.query(User).filter_by(id=userid).first()

    if player_data:
        return render_template(template_name, data=[player_data])
    else:
        return render_template(template_name, fail_message='Player with id %s does not exists.' % userid)


@app.route("/players/<userid>/edit", methods=["GET"])
def edit_user_info(userid):
    template_name = 'edit_user.html'
    session = db.session()
    player_data = session.query(User).filter_by(id=userid).first()

    if player_data:
        return render_template(template_name, data=[player_data])
    else:
        return render_template(template_name, fail_message='Player with id %s does not exists.' % userid)


@app.route("/players/<userid>/edit", methods=["POST"])
def submit_edit_user_info(userid):
    session = db.session()
    name = request.form.get("name")

    if not name:
        return render_template("register.html", fail_message="Name cannot be empty.")

    player = session.query(User).filter_by(id=userid).first()
    player.name = name
    db.session.commit()

    return render_template("register.html", success_message="Successfully edited player %s" % userid)

# todo: endpoint turnauslistan luomiseen


@app.route("/create_list", methods=["GET"])
def create_list_give_player_names():
    # todo: filter players that are not in some other tournament
    session = db.session()
    players = [p.name for p in session.query(User).all()]
    return jsonify(players)
