from app import db
import enum

class User(db.Model):
    __table_args__ = {'extend_existing': True}
    name = db.Column(db.String(100),  primary_key =True, unique=True)
    time = db.Column(db.Integer)
    date = db.Column(db.String(20))

    def __repr__(self):
        return '<Title: {self.name}>'