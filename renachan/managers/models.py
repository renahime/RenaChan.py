import os
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, DateTime, Table, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Define the association table for the many-to-many relationship
member_server_association = Table('member_server_association', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id')),
    Column('server_id', Integer, ForeignKey('servers.id')),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

# Define the association table for the many-to-many relationship between Member and Finder
member_finder_association = Table('member_finder_association', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id')),
    Column('finder_id', Integer, ForeignKey('finders.finder_id')),
    Column('server_id', Integer, ForeignKey('servers.id')),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

# Define the association table for the many-to-many relationship between Member and ToDo
member_todo_association = Table('member_todo_association', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id')),
    Column('todo_id', Integer, ForeignKey('to_dos.todo_id')),
    Column('server_id', Integer, ForeignKey('servers.id')),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

# Define the association table for the many-to-many relationship between Member and Tracker
member_tracker_association = Table('member_tracker_association', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id')),
    Column('tracker_id', Integer, ForeignKey('trackers.tracker_id')),
    Column('server_id', Integer, ForeignKey('servers.id')),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

# Define the association table for the many-to-many relationship between Member and Session
member_session_association = Table('member_session_association', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id')),
    Column('session_id', Integer, ForeignKey('sessions.session_id')),
    Column('server_id', Integer, ForeignKey('servers.id')),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    server_name = Column(String)

    # One Server can have many Channels
    channels = relationship('Channel', back_populates='server')

    # One Server can have many Members
    members = relationship('Member', secondary=member_server_association, back_populates='servers')

    # One Server belongs to an Owner
    owner = relationship('Owner', back_populates='servers')

    # One Server can have many Finders
    finders = relationship('Finder', secondary=member_finder_association, back_populates='server')

    # One Server can have many ToDos
    to_dos = relationship('ToDo', secondary=member_todo_association, back_populates='server')

    # One Server can have many Sessions
    sessions = relationship('Session', secondary=member_session_association, back_populates='server')

    # One Server can have many Trackers
    trackers = relationship('Tracker', secondary=member_tracker_association, back_populates='server')

    def to_dict(self):
        return {
            'server_id': self.id,
            'owner_id': self.owner_id,
            'server_name': self.server_name
        }

class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    username = Column(Integer)
    user_discriminator = Column(Integer)

    # One Owner can have many Servers
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

    # One Member can have many Finders
    finders = relationship('Finder', secondary=member_finder_association, back_populates='members')

    # One Member can have many ToDos
    to_do = relationship('ToDo', secondary=member_todo_association, back_populates='members')

    # One Member can have many Trackers
    trackers = relationship('Tracker', secondary=member_tracker_association, back_populates='members')

    # One Member can have many Sessions
    sessions = relationship('Session', secondary=member_session_association, back_populates='members')

    # One Member can belong to many Servers through the association table
    servers = relationship('Server', secondary=member_server_association, back_populates='members')

    def to_dict(self):
        return {
            'member_id': self.id,
            'username': self.username,
            'user_discriminator': self.user_discriminator
        }

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    channel_name = Column(String)

    # One Channel can have One Server
    server = relationship('Server', back_populates='channels')

    def to_dict(self):
        return {
            'channel_id': self.id,
            'server_id': self.server_id,
            'channel_name': self.channel_name,
        }

class Finder(Base):
    __tablename__ = 'finders'
    finder_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    chosen_url = Column(String)
    last_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    # One Finder can have One Server
    server = relationship('Server', back_populates='finders')

    # Many Finders can belong to many Members through the association table
    members = relationship('Member', secondary=member_finder_association, back_populates='finders')

    def to_dict(self):
        return {
            'finder_id': self.finder_id,
            'server_id': self.server_id,
            'date': self.date,
            'chosen': self.chosen_url,
            'last_time': self.last_time
        }

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    duration = Column(Integer)

    # One Session can have One Server
    server = relationship('Server', back_populates='sessions')

    # Many Sessions can belong to many Members through the association table
    members = relationship('Member', secondary=member_session_association, back_populates='sessions')

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'user_id': self.member_id,
            'date': self.date,
            'duration': self.duration,
        }

class ToDo(Base):
    __tablename__ = 'to_dos'
    todo_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    to_do = Column(String)
    due = Column(DateTime)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    duration = Column(DateTime)

    # One ToDo can have One Server
    server = relationship('Server', back_populates='to_dos')

    # Many ToDos can belong to many Members through the association table
    members = relationship('Member', secondary=member_todo_association, back_populates='to_do')

    def to_dict(self):
        return {
            'session_id': self.todo_id,
            'user_id': self.member_id,
            'to_do': self.to_do,
            'date': self.date,
            'due': self.due,
            'duration': self.duration
        }

class Tracker(Base):
    __tablename__ = 'trackers'
    tracker_id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    track_url = Column(String)
    title= Column(String)
    available= Column(Boolean)
    price= Column(Float)
    last_checked = Column(DateTime, nullable=False, default=datetime.utcnow)

    # One Tracker can have One Server
    server = relationship('Server', back_populates='trackers')

    # Many Trackers can belong to many Members through the association table
    members = relationship('Member', secondary=member_tracker_association, back_populates='trackers')

    def to_dict(self):
        return {
            'tracker_id': self.tracker_id,
            'server_id': self.server_id,
            'track_url': self.track_url,
            'available': self.available,
            'title': self.title,
            'price': self.price,
            'last_checked': self.last_checked,
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
