from flask import render_template, request, jsonify
from application import app, db
from application.rankings.models import Player


@app.route("/")
def index():
    return render_template('index.html', players=Player.query.all())


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def create_player():
    name = request.form.get('name')
    if not name:
        return render_template("register.html", fail_message="Name cannot be empty.")

    session = db.session()
    is_existing = session.query(Player).filter_by(name=name).first()

    if is_existing:
        return render_template("register.html", fail_message='Player %s already exists.' % name)

    p = Player(name)
    db.session().add(p)
    db.session().commit()

    return render_template("register.html", success_message="Successfully added player %s." % p.name)


# todo: endpoint turnauslistan luomiseen

@app.route("/create_list", methods=["GET"])
def create_list_give_player_names():
    # todo: filter players that are not in some other tournament
    session = db.session()
    players = [p.name for p in session.query(Player).all()]
    return jsonify(players)