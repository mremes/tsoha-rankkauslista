from flask import render_template, request
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
    p = Player(request.form.get('name'))

    db.session().add(p)
    db.session().commit()

    return "Successfully added player " + p.name
