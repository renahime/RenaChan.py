from .database import db
from datetime import datetime


i_like = db.Table(
    "i_like",
    db.Column(
        "finder_id",
        db.Integer,
        db.ForeignKey("finders.id"),
        primary_key=True
    ),
    db.Column(
        "i_like_url",
        db.String
    )
)


class Finder(db.Model):
    __tablename__ = 'finders'

    finder_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.channel_id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    chosen = db.Column(db.String)
    last_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', back_populates='finder')
    channel = db.relationship('Channel', back_populates='finder')

    def to_dict(self):
        return {
            'session_id': self.finder_id,
            'user_id': self.user_id,
            'channel_id': self.channel_id,
            'date': self.date,
            'chosen': self.chosen,
            'last_time': self.last_time
            }
