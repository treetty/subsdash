from flask_sqlalchemy import SQLAlchemy

from subsdash.extensions import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    answer = db.Column(db.String(4), nullable=True)

    def __init__(self, pid, answer):
        self.pid = pid
        self.answer = answer
