from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the RenaBot package to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the metadata to ensure it is recognized by Alembic
from renachan.managers.database import metadata

# This is the 'offline' SQLAchemy URL to use while running migrations.
# Replace it with the correct path to your dev.db file.
# For example, sqlite:////path/to/RenaBot/renachan/dev.db
offline_url = "sqlite:///" + os.path.join(os.path.dirname(__file__), "renachan", "dev.db")

# Configure Alembic to use the offline URL
config = context.config
config.set_main_option("sqlalchemy.url", offline_url)

# Use a custom version table to track migration versions in the database
config.set_main_option("version_table", "alembic_version")

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Run the migrations with the given configuration
target_metadata = metadata


def run_migrations_online():
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_online()
