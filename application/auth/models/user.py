from application import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_dt = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name: str, username: str, role: str, password: str):
        self.name = name
        self.username = username
        self.role = role
        self.password = password

    def check_password(self, input_password):
        if self.password == input_password:
            return True
        return False

    def get_id(self):
        return self.id

    def roles(self):
        return ["ADMIN", "PLAYER", "TOURNAMENT"]
