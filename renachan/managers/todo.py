# TABLES['channels'] = (
#     "CREATE TABLE IF NOT EXISTS `channels` ("
#     "  `channel_id` int(18) NOT NULL,"
#     "  `channel_name` TINYTEXT NOT NULL,"
#     ") ENGINE=InnoDB")

from .database import db
from datetime import datetime


class ToDo(db.Model):
    __tablename__ = 'to_do'

    todo_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.channel_id'))
    to_do = db.Column(db.String)
    due = db.Column(db.DateTime)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='to_do')
    channel = db.relationship('Channel', back_populates='to_do')

    def to_dict(self):
        return {
            'session_id': self.todo_id,
            'user_id': self.user_id,
            'to_do': self.to_do,
            'date': self.date,
            'due' :self.due,
            'duration': self.duration
        }
