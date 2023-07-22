import os
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from renachan.managers.models import Base, Server, Owner, Member, Channel, i_like, i_might, Finder, Session, ToDo


def initialize_database():
    # Get the base directory path of the current file (database.py)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construct the path to the dev.db file inside the renachan directory
    db_file = "dev.db"
    db_path = os.path.join(base_dir, db_file)

    # Create a session to return to the bot
    # SQLAlchemy
        ### SQLAlchemy is an Object-Relational Mapping (ORM) library for Python, which allows you to interact with databases using Python objects instead of writing raw SQL queries.
        ### Since we are using a SQLite engine for testing, this means we'll be connecting to an SQLite database.
        ### SQLite is a lightweight, file-based database system that doesn't require a separate server; it's often used for smaller applications or prototyping.

    ## create_engine() - This function is used to create a new SQLAlchemy engine. It takes a URL-like string as its argument, specifying the database connection details.
    ## "sqlite:///" - The URL-like string used here is a SQLite database connection URL. The sqlite:// part indicates that you want to use the SQLite dialect (driver) for the database engine.
    ## "/{db_path}" - The {db_path} is a placeholder representing the path to the SQLite database file. It is provided using Python's string formatting with an "f-string" (formatted string literal) where the f prefix allows you to include expressions inside curly braces {}.

    ### So, when create_engine() is called with the formatted URL, it creates an engine connected to the dev.db file, allowing you to interact with the SQLite database through SQLAlchemy's API.
    engine = create_engine(f"sqlite:///{db_path}")


    # sessionmaker
    ## The sessionmaker is a factory class provided by SQLAlchemy.
        ## Factory classes is a class that is responsible for creating objects of another class or a group of related classes.
        ## It is a creational design pattern that helps encapsulate the object creation process and provides a centralized place for creating instances.

    # bind=engine
    ## The bind parameter in the sessionmaker constructor allows you to specify the database engine to which the session objects should be bound.
    ## In this case, we are binding the sessions to the engine you created earlier using create_engine().
    ## It means that any operations performed with this session will be executed on the database connected through the specified engine.

    # Session = sessionmaker(bind=engine)
    ## It is used to generate new session objects that will be bound to a specific database engine (engine).
    ## When you call sessionmaker(bind=engine), you are creating a session factory that knows how to create sessions associated with the specified database engine.
    ## Since this is coming from a factory class this is not exactly making the instance of the class but rather creating the class itself.
    Session = sessionmaker(bind=engine)

    # Session()
    ## This line creates a new session instance using the Session class we defined earlier.
    ## It effectively opens a connection to the database (if it's not already open) and provides you with a session object through which you can perform database operations.
    ## Since we have recieved the Session class from the line before we can now create an instance of the Session class here, which is what we will use to to work with the database.
    ## If the dev.db file already exists at the specified path, the engine will connect to it.
    ## If the file doesn't exist, SQLAlchemy will create it at that location. So, at this step, the dev.db file is created if it doesn't already exist.
    session = Session()

    try:
        # MetaData
        ## MetaData is a class in SQLAlchemy that represents a collection of database schema information.
        ## It acts as a container to hold metadata about the structure of a database, including tables, columns, and other database constructs.

        # Check if all tables and columns are correct
        # MetaData(bind=engine)
        ## This creates a new MetaData instance and binds it to a specific database engine (engine).
        ## By binding MetaData to the engine, SQLAlchemy knows which database engine to use when it needs to retrieve the database schema information.
        metadata = MetaData(bind=engine)

        # metadata.reflect()
        ## When this function is called SQLAlchemy retrieves the schema information from the database engine (engine) to populate the metadata object with Table objects representing each table in the database.
        ## Each Table object contains information about its columns, constraints, and other metadata.

        # Why use reflection?
        ## Reflection is particularly useful when you want to work with an existing database without having to manually define SQLAlchemy models for each table.
        ## By reflecting the schema, you can dynamically interact with the database using the metadata object and perform queries without writing explicit model definitions.
        ## The process of reflection gathers information from the database and populates the metadata object with Table objects, making it a valuable tool for dynamically interacting with the database without explicitly defining model classes.
        metadata.reflect()

        # List of table names that should be present in the database
        expected_tables = [
            'servers',
            'owners',
            'members',
            'channels',
            'i_like',
            'i_might_like',
            'finders',
            'sessions',
            'to_dos',
            'member_server_association',
            'trackers'
        ]

        # Check if all expected tables exist in the database
        missing_tables = set(expected_tables) - set(metadata.tables.keys())
        if not missing_tables and os.path.exists(db_path):
            # All expected tables are present, no need to recreate them
            logging.info("Database found and ready to use")
            return session
        else:
            # Base
            ## This is the base class that serves as the parent for all your SQLAlchemy model classes.
            ## It is typically created using the declarative_base() function from SQLAlchemy. When you define your model classes, you should make them subclasses of Base.
            ## This allows SQLAlchemy to track your model classes and their associated database tables.

            # Base.metadata
            ## This is an attribute of the Base class that holds the metadata associated with your models.
            ## It includes information about all the tables, columns, and other database constructs defined in your model classes.

            # create_all(engine)
            ## This is a method is a convenience method provided by SQLAlchemy's MetaData object to create the database tables based on the model definitions.
            ## It takes an engine as its argument and uses that engine to execute the SQL commands necessary to create the tables in the connected database.
            # Some tables are missing, create them

            # Conclusion
            ## SQLAlchemy will use the metadata associated with your model classes (Base.metadata) to create the necessary tables in the SQLite database represented by the engine.
            Base.metadata.create_all(engine)
            logging.info("Database is missing... creating tables as needed")
            return session

    except OperationalError as e:
        logging.error(f"Error while initializing the database: {e}")
        return None


# Example usage:
if __name__ == "__main__":
    session = initialize_database()
