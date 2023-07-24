import os
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, DateTime, Table, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()



# Sure! ISO 8601 is an international standard for representing dates and times.
# It defines a standard format for date and time representations, making it easier
# for different systems and programming languages to understand and exchange date and time information consistently.
# When working with date and time data in databases or APIs, using the ISO 8601 format for representing dates and times has several advantages:




member_server_association = Table('member_server_association', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id')),
    Column('server_id', Integer, ForeignKey('servers.id')),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    server_name = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    channels = relationship('Channel', back_populates='server')
    members = relationship('Member', secondary=member_server_association, back_populates='servers')
    owner = relationship('Owner', back_populates='servers')
    finders = relationship('Finder', back_populates='server')
    to_dos = relationship('ToDo', back_populates='server')
    sessions = relationship('Session', back_populates='server')
    trackers = relationship('Tracker', back_populates='server')

    def to_dict(self):
        return {
            'server_id': self.id,
            'owner_id': self.owner_id,
            'server_name': self.server_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    username = Column(Integer)
    user_discriminator = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    servers = relationship('Server', back_populates='owner')

    def to_dict(self):
        return {
            'owner_id': self.id,
            'username': self.username,
            'user_discriminator': self.user_discriminator,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    username = Column(Integer)
    user_discriminator = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    finders = relationship('Finder', back_populates='member')
    to_do = relationship('ToDo', back_populates='member')
    trackers = relationship('Tracker', back_populates='member')
    sessions = relationship('Session', back_populates='member')
    servers = relationship('Server', secondary=member_server_association, back_populates='members')

    def to_dict(self):
        return {
            'member_id': self.id,
            'username': self.username,
            'user_discriminator': self.user_discriminator,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    channel_name = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    server = relationship('Server', back_populates='channels')

    def to_dict(self):
        return {
            'channel_id': self.id,
            'server_id': self.server_id,
            'channel_name': self.channel_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Finder(Base):
    __tablename__ = 'finders'
    finder_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    member_id = Column(Integer, ForeignKey('members.id'))
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    chosen_url = Column(String)
    last_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    server = relationship('Server', back_populates='finders')
    member = relationship('Member', back_populates='finders')

    def to_dict(self):
        return {
            'finder_id': self.finder_id,
            'server_id': self.server_id,
            'member_id': self.member_id,
            'date': self.date,
            'chosen': self.chosen_url,
            'last_time': self.last_time,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    member_id = Column(Integer, ForeignKey('members.id'))
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    duration = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    server = relationship('Server', back_populates='sessions')
    member = relationship('Member', back_populates='sessions')

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'server_id': self.server_id,
            'member_id': self.member_id,
            'date': self.date,
            'duration': self.duration,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ToDo(Base):
    __tablename__ = 'to_dos'
    todo_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    member_id = Column(Integer, ForeignKey('members.id'))
    to_do = Column(String)
    due = Column(DateTime)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    duration = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    server = relationship('Server', back_populates='to_dos')
    member = relationship('Member', back_populates='to_do')

    def to_dict(self):
        return {
            'todo_id': self.todo_id,
            'server_id': self.server_id,
            'member_id': self.member_id,
            'to_do': self.to_do,
            'date': self.date,
            'due': self.due,
            'duration': self.duration,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Tracker(Base):
    __tablename__ = 'trackers'
    tracker_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    member_id = Column(Integer, ForeignKey('members.id'))
    track_url = Column(String)
    title = Column(String)
    available = Column(Boolean)
    price = Column(Float)
    last_checked = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    server = relationship('Server', back_populates='trackers')
    member = relationship('Member', back_populates='trackers')


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
