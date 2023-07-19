# TABLES['channels'] = (
#     "CREATE TABLE IF NOT EXISTS `channels` ("
#     "  `channel_id` int(18) NOT NULL,"
#     "  `channel_name` TINYTEXT NOT NULL,"
#     ") ENGINE=InnoDB")

from .database import db


class Channel(db.Model):
    __tablename__ = 'channels'

    channel_id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String)

    session = db.relationship('Channel', back_populates='channel')
    finder = db.relationship('Finder', back_populates='channel')
    to_do = db.relationship('ToDo', back_populates='channel')

    def to_dict(self):
        return {
            'channel_id': self.channel_id,
            'channel_name': self.channel_name,
            }
