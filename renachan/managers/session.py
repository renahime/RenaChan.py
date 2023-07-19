# TABLES['channels'] = (
#     "CREATE TABLE IF NOT EXISTS `channels` ("
#     "  `channel_id` int(18) NOT NULL,"
#     "  `channel_name` TINYTEXT NOT NULL,"
#     ") ENGINE=InnoDB")

from .database import db
from datetime import datetime


class Session(db.Model):
    __tablename__ = 'channels'

    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.channel_id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer)

    user = db.relationship('User', back_populates='session')
    channel = db.relationship('Channel', back_populates='session')

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'date': self.date,
            'duration': self.duration,
            }
