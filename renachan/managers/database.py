import os
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from alembic.config import Config
from alembic import command
import shutil

Base = declarative_base()

# Get the base directory path of the current file (database.py)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Construct the path to the renachan folder
renachan_dir = os.path.join(base_dir, 'renachan')

# Construct the path to the dev.db file inside the renachan directory
db_file = "dev.db"
db_path = os.path.join(renachan_dir, db_file)

# Construct the path to the alembic directory inside the renachan folder
alembic_dir = os.path.join(base_dir, 'alembic')

# Create the engine and metadata objects once
engine = create_engine(f"sqlite:///{db_path}")
metadata = MetaData(bind=engine)

def create_migration_version_file():
    # Check if the alembic directory exists, and if not, create it
    if not os.path.exists(alembic_dir):
        os.makedirs(alembic_dir)

    # Check if the 'versions' directory exists in the alembic folder, and if not, create it
    alembic_versions_dir = os.path.join(alembic_dir, 'versions')
    if not os.path.exists(alembic_versions_dir):
        os.makedirs(alembic_versions_dir)

    # Create and configure the Alembic configuration
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))

    # Get the current alembic version from the database
    current_version = command.current(alembic_cfg, revision='head')

    # Check if the current version is None (no migration version found) or different from the latest version
    if not current_version or current_version != renachan.version():
        # Generate a new migration script based on the differences between the current schema and the models
        command.revision(alembic_cfg, autogenerate=True, message="initial migration")


def check_migration_version_files():
    # Check if the 'alembic_version' table exists in the database
    version_table = Table('alembic_version', metadata, Column('version_num', String(32), nullable=False))
    return engine.dialect.has_table(engine, version_table.name)

def run_migrations(session=None):
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))

    # Check if there are any migration version files inside the 'alembic/versions' directory
    if not check_migration_version_files():
        # If there are no migration version files, create and run migrations
        command.upgrade(alembic_cfg, "head", sql=False, tag=None)
    else:
        # If the 'alembic_version' table exists in the database, perform migrations if needed
        with session.begin():
            if not command.current(alembic_cfg, revision='head', connection=session.connection()):
                command.upgrade(alembic_cfg, "head", sql=False, tag=None)

def initialize_database():
    if not os.path.exists(db_path):
        # If the database does not exist, create a new database and tables in the RenaChan folder
        Base.metadata.create_all(engine)
        # Create the migration version file
        create_migration_version_file()
        # Perform the initial migration
        run_migrations()
    else:
        # If the database exists, check if it's the correct version and perform migrations if needed
        alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
        alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))

        # Check if there are any migration version files inside the 'alembic/versions' directory
        if not check_migration_version_files():
            create_migration_version_file()
            run_migrations()
        else:
            # If the 'alembic_version' table exists in the database, perform migrations if needed
            with engine.begin() as connection:
                if not command.current(alembic_cfg, revision='head', connection=connection):
                    run_migrations()

def get_database():
    global engine
    initialize_database()

    # Create and return a scoped session
    Session = scoped_session(sessionmaker(bind=engine))
    return Session()
