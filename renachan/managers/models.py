import os
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Server(Base):
      __tablename__ = 'servers'
      id = Column(Integer, primary_key=True)
      owner_id = Column(Integer, ForeignKey("owners.id"))
      server_name = Column(String)

      session = relationship('Session', back_populates='server')
      to_do = relationship('ToDo', back_populates='server')
      finder = relationship('Finder', back_populates='server')
      channels = relationship('Channel', back_populates='server')
      owner = relationship('Owner', back_populates='servers')

class Owner(Base):
      __tablename__ = 'owners'
      id = Column(Integer, primary_key=True)
      username = Column(Integer)
      user_discriminator = Column(Integer)

      servers = relationship('Server', back_populates='owner')

      def to_dict(self):
          return {
              'owner_id': self.id,
              'username': self.username,
              'user_discriminator': self.user_discriminator
              }

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    username = Column(Integer)
    user_discriminator = Column(String)

    session = relationship('Session', back_populates='member')
    to_do = relationship('ToDo', back_populates='member')
    finder = relationship('Finder', back_populates='member')
    server = relationship('Server', back_populates='member')

    def to_dict(self):
          return {
              'user_id': self.id,
              'user_name': self.username,
              'user_discriminator': self.user_discriminator
              }

class Channel(Base):
      __tablename__ = 'channels'
      id = Column(Integer, primary_key=True)
      server_id = Column(Integer, ForeignKey('servers.id'))
      channel_name = Column(String)

      server = relationship('Server', back_populates='channels')

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
         'member_id',  # Corrected table name here
         Integer,
         ForeignKey("members.id")  # Corrected table name here
    ),
    Column(
        "i_like_url",
        String
    ),
    Column(
         "i_like_site",
         String
    ),
    Column(
         "i_like_title",
         String
    )
)

i_might = Table(
    "i_might_like", Base.metadata,
    Column(
        "finder_id",
        Integer,
        ForeignKey("finders.finder_id"),  # Update the foreign key reference to 'finders.finder_id'
        primary_key=True
    ),
    Column(
         'member_id',  # Corrected table name here
         Integer,
         ForeignKey("members.id")  # Corrected table name here
    ),
    Column(
        "i_might_like_url",
        String
    ),
    Column(
         "i_might_like_site",
         String
    ),
    Column(
         "i_might_like_table",
         String
    )
)




class Finder(Base):
      __tablename__ = 'finders'
      finder_id = Column(Integer, primary_key=True)
      user_id = Column(Integer, ForeignKey('members.id'))
      server_id = Column(Integer, ForeignKey('servers.id'))
      date = Column(DateTime, nullable=False, default=datetime.utcnow)
      chosen_url = Column(String)
      last_time = Column(DateTime, nullable=False, default=datetime.utcnow)

      member = relationship('Member', back_populates='finder')
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
    __tablename__ = 'sessions'  # Correct table name here
    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('members.id'))
    server_id = Column(Integer, ForeignKey('servers.id'))
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    duration = Column(Integer)

    member = relationship('Member', back_populates='session')
    server = relationship('Server', back_populates='session')

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'date': self.date,
            'duration': self.duration,
        }

class ToDo(Base):
      __tablename__ = 'to_dos'
      todo_id = Column(Integer, primary_key=True)
      user_id = Column(Integer, ForeignKey('members.id'))
      server_id = Column(Integer, ForeignKey('servers.id'))
      to_do = Column(String)
      due = Column(DateTime)
      date = Column(DateTime, nullable=False, default=datetime.utcnow)
      duration = Column(DateTime)

      member = relationship('Member', back_populates='to_do')
      server = relationship('Server', back_populates='to_do')
      def to_dict(self):
          return {
              'session_id': self.todo_id,
              'user_id': self.user_id,
              'to_do': self.to_do,
              'date': self.date,
              'due' :self.due,
              'duration': self.duration
          }
