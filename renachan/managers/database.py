from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///dev.db', echo=True)


class Server(Base):
      __tablename__ = 'servers'
      __table_args__ = {'extend_existing': True}
      id = Column(Integer, primary_key=True)
      owner_id = Column(Integer, ForeignKey("users.id"))
      server_name = Column(String)

      session = relationship('Session', back_populates='server')
      to_do = relationship('ToDo', back_populates='server')
      finder = relationship('Finder', back_populates='server')
      channels = relationship('Channel', back_populates='server')
      owner = relationship('Owner', back_populates='servers')

class Owner(Base):
      __tablename__ = 'users'
      __table_args__ = {'extend_existing': True}
      id = Column(Integer, primary_key=True)
      username = Column(Integer)
      user_discriminator = Column(Integer)

      server = relationship('Server', back_populates='owner')

      def to_dict(self):
          return {
              'owner_id': self.user_id,
              'username': self.user_name,
              'user_discriminator': self.user_discriminator
              }

class Member(Base):
    __tablename__ = 'members'
    __table_args__ = {'extended_existing': True}
    id = Column(Integer, primary_key=True)
    username = Column(Integer)
    user_discriminator = Column(Integer)

    session = relationship('Session', back_populates='user')
    to_do = relationship('ToDo', back_populates='user')
    finder = relationship('Finder', back_populates='user')
    server = relationship('Server', back_populates='user')

    def to_dict(self):
          return {
              'user_id': self.user_id,
              'user_name': self.user_name,
              'user_discriminator': self.user_discriminator
              }

class Channel(Base):
      __tablename__ = 'channels'
      __table_args__ = {'extend_existing': True}
      id = Column(Integer, primary_key=True)
      server_id = Column(Integer, ForeignKey('servers.id'))
      channel_name = Column(String)

      session = relationship('Channel', back_populates='channel')
      finder = relationship('Finder', back_populates='channel')
      to_do = relationship('ToDo', back_populates='channel')
      server = relationship('Server', back_populates='chennels')

      def to_dict(self):
          return {
              'channel_id': self.channel_id,
              'channel_name': self.channel_name,
              }

i_like = Table(
    "i_like", Base.metadata,
    Column(
        "finder_id",
        Integer,
        ForeignKey("finders.finder_id"),  # Update the foreign key reference to 'finders.finder_id'
        primary_key=True
    ),
    Column(
        "i_like_url",
        String
    )
)



class Finder(Base):
      __tablename__ = 'finders'
      __table_args__ = {'extend_existing': True}
      finder_id = Column(Integer, primary_key=True)
      user_id = Column(Integer, ForeignKey('users.id'))
      channel_id = Column(Integer, ForeignKey('channels.id'))
      server_id = Column(Integer, ForeignKey('servers.id'))
      date = Column(DateTime, nullable=False, default=datetime.utcnow)
      chosen_url = Column(String)
      last_time = Column(DateTime, nullable=False, default=datetime.utcnow)

      owner = relationship('User', back_populates='finder')
      channel = relationship('Channel', back_populates='finder')
      server = relationship('Server', back_populates='finder')

      def to_dict(self):
          return {
              'session_id': self.finder_id,
              'user_id': self.user_id,
              'channel_id': self.channel_id,
              'date': self.date,
              'chosen': self.chosen,
              'last_time': self.last_time
          }

class Session(Base):
      __tablename__ = 'channels'
      __table_args__ = {'extend_existing': True}
      session_id = Column(Integer, primary_key=True)
      user_id = Column(Integer, ForeignKey('users.id'))
      channel_id = Column(Integer, ForeignKey('channels.id'))
      server_id = Column(Integer, ForeignKey('servers.id'))
      date = Column(DateTime, nullable=False, default=datetime.utcnow)
      duration = Column(Integer)

      owner = relationship('User', back_populates='session')
      channel = relationship('Channel', back_populates='session')

      def to_dict(self):
          return {
              'session_id': self.session_id,
              'user_id': self.user_id,
              'date': self.date,
              'duration': self.duration,
              }

class ToDo(Base):
      __tablename__ = 'to_do'
      __table_args__ = {'extend_existing': True}
      todo_id = Column(Integer, primary_key=True)
      user_id = Column(Integer, ForeignKey('users.id'))
      channel_id = Column(Integer, ForeignKey('channels.id'))
      server_id = Column(Integer, ForeignKey('servers.id'))
      to_do = Column(String)
      due = Column(DateTime)
      date = Column(DateTime, nullable=False, default=datetime.utcnow)
      duration = Column(DateTime)

      owner = relationship('User', back_populates='to_do')
      channel = relationship('Channel', back_populates='to_do')

      def to_dict(self):
          return {
              'session_id': self.todo_id,
              'user_id': self.user_id,
              'to_do': self.to_do,
              'date': self.date,
              'due' :self.due,
              'duration': self.duration
          }

def create_database():
  #  connect in memory sqlite database or you can connect your own database
  Base.metadata.create_all(engine)

  # create session and bind engine
  session = sessionmaker(bind=engine)
  return session
