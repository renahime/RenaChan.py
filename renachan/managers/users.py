# TABLES['users'] = (
#     "CREATE TABLE IF NOT EXISTS `users` ("
#     "  `user_id` int(18) NOT NULL,"
#     "  `user_name` TINYTEXT NOT NULL,"
#     "  `user_discriminator` int(4) NOT NULL,"
#     ") ENGINE=InnoDB")


from .database import db


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer)
    user_discriminator = db.Column(db.Integer)

    session = db.relationship('Session', back_populates='user')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_discriminator': self.user_discriminator
            }
