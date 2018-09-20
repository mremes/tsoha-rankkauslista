from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application.extensions import csrf

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="G!DD,1c]L?5[pagF}ohmlo.EDG0MP%`&{Nbc91""A^Vl=Q{99[aE~w+~c={H@+#",
    WTF_CSRF_SECRET_KEY="W~K%pS}lJxX)vkI-[p0nzPdrwvPyPXitUD!XY3A`._[-RG=[&V9*n3~w0HX./:g"
))

csrf.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rankings.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

migrate = Migrate(app, db)

db.create_all()

from application.auth.login import login_manager
login_manager.init_app(app)
