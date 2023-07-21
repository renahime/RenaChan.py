import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from renachan.managers.models import Base, Server, Owner, Member, Channel, i_like, i_might, Finder, Session, ToDo

def initialize_database():
    # Get the base directory path of the current file (database.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the renachan folder
    renachan_dir = os.path.join(base_dir, 'renachan')

    # Construct the path to the dev.db file inside the renachan directory
    db_file = "dev.db"
    db_path = os.path.join(renachan_dir, db_file)

    # Check if the dev.db file exists
    if not os.path.exists(db_path):
        # Create the database
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)

    # Create a session to return to the bot
    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if all tables and columns are correct
    metadata = MetaData(bind=engine)
    metadata.reflect()

    # List of table names that should be present in the database
    expected_tables = [
        'servers',
        'owners',
        'members',
        'channels',
        'i_like',
        'i_might',
        'finder',
        'sessions',
        'todo'
    ]

    # Check if all expected tables exist in the database
    if set(expected_tables) <= set(metadata.tables.keys()):
        return session
    else:
        # Some tables are missing or incorrect, fix the dev.db file to match the models
        # (You might need to add migration logic here depending on the changes to the models)
        # For simplicity, we'll just drop all tables and recreate them
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        return session

# Example usage:
if __name__ == "__main__":
    session = initialize_database()
