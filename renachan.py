## renachan.py
### This script is the core of the RenaChan.py Discord bot.
### It sets up the necessary imports, environment variables, and logging.
### It fetches the latest version information from the GitHub repository, initializes the database, loads event handlers and command implementations.
### Finally, it creates and runs the Discord bot with the specified configuration.
### The bot is designed to respond to various events and user commands on Discord, providing functionality based on its configuration and the user's interactions.

### The bot script by setting up imports and the logging configuration. This ensures that necessary libraries and modules are available and sets up a basic logging system to track events
### in the bot's execution.
import os
import sys
import requests
import json
import logging
from make_logger import initialize_logger

### os, sys, requests, json, logging: These are standard Python libraries that provide various functionalities for handling operating system tasks, making HTTP requests,
### working with JSON data, and logging.

import discord
from discord.ext import commands
### discord, discord.ext.commands: These are part of the Discord.py library, which allows interaction with the Discord API and simplifies creating a Discord bot.

from dotenv import load_dotenv
from os.path import join, dirname
### dotenv: This library loads environment variables from a .env file into the bot's runtime environment.


# Set up the logging configuration
logger = initialize_logger()
### The sys.path list contains strings that represent directory paths. When you attempt to import a module,
### Python searches for that module in each directory listed in sys.path in the order they appear in the list.
### You can view more about sys.path here https://docs.python.org/3/library/sys.html#sys.path

# Add the parent directory to sys.path

##  __file__
### In Python, __file__ is a built-in variable that represents the path of the current Python script (module) being executed.
### It contains the absolute or relative path to the script file.

##  os.path.abspath(__file__)
### The os.path.abspath() function takes a file path as input and returns the absolute version of that path.
### If the original path is already absolute, it is returned unchanged.
### If it is a relative path, the function converts it to an absolute path based on the current working directory.

##  os.path.dirname(os.path.abspath(__file__))
### The os.path.dirname() function extracts the directory part of a given file path. It takes a file path as input and returns the directory path containing the file.

### This gives you the absolute path to the directory containing the current Python script. This is useful for various
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# print(sys.path) ## [list of directories]
# print(os.path.dirname(os.path.abspath(__file__))) ## /home/rena/appacademy/Projects/RenaBot


## join(dirname(__file__), '.env')
### The join() function from the os.path module combines the directory path obtained in step 3 with the filename '.env' to form the absolute path to the .env file.
### This is done to ensure that the .env file is located in the same directory as the script.

##  load_dotenv(join(dirname(__file__), '.env'))
### load_dotenv() function from the dotenv library loads the environment variables from the specified .env file (the one obtained in step 4) into the runtime environment of the script.
### This allows the script to access and use environment variables defined in the .env file during its execution.
load_dotenv(join(dirname(__file__), '.env'))

from renachan import renachan  # Import renachan package
from renachan.managers.database import initialize_database

## renachan:
### A package is a way to organize Python modules in a directory. It is a collection of Python modules and may contain a __init__.py file (not to be confused with the .env file).
### The package here contains the main functionality of the bot, and the renachan module inside this package is imported for use in the script.
### A module is a file containing Python definitions and statements

## renachan.managers.database:
### This is a module within the renachan package responsible for managing the bot's database.
### The initialize_database() function from this module will be used later to initialize the database.

def main():
    """
    The entry point of the RenaChan.py Discord bot.

    This function performs the following tasks:
        1. Calls the 'check_latest_version()' function to check if the bot is running the latest version.
        2. Calls the 'setup_bot()' function to set up the Discord bot with the necessary configurations and event handlers.
        3. Initializes the bot by running it with 'bot.run(renachan.config.bot_token())'.
        4. Logs a message indicating that the bot is initializing.
        5. Catches any exceptions that occur during the bot's execution and logs an error message along with the exception details.

    Notes:
        - 'check_latest_version()': This function checks the latest version of RenaChan.py on GitHub and logs a message based on whether the bot is running the latest version or not.
        - 'setup_bot()': This function sets up the Discord bot with the necessary configurations, event handlers, and presence.
        - 'bot.run()': This call starts the bot's connection to Discord and starts processing events.
        - Exceptions: The 'try' block catches any exceptions that occur during the bot's execution. If an exception is caught, it logs an error message and exits with status code 1.
    """

    try:
        # Calls the 'check_latest_version()' function to check if the bot is running the latest version.
        check_latest_version()

        # Calls the 'setup_bot()' function to set up the Discord bot with the necessary configurations and event handlers.
        bot = setup_bot()

        # Logs a message indicating that the bot is initializing.
        logger.info("Initializing bot...")

        # Initializes the bot by running it with 'bot.run(renachan.config.bot_token())'.
        bot.run(renachan.config.bot_token())

    except Exception as e:
        # Catches any exceptions that occur during the bot's execution and logs an error message along with the exception details.
        logger.error(f"[/!\\] Error: Failed to run bot!\n{e}")

        # Exits the script with status code 1 to indicate an error.
        exit(1)

def check_latest_version():
    """
    Checks the latest version of RenaChan.py on GitHub and logs the status.

    This function makes an API request to the GitHub repository of RenaChan.py to fetch the latest version tags.
    It then compares the latest version with the current version of the bot to determine if the user is running the latest version or not.
    The comparison results are logged to provide feedback to the user.

    Note:
        - The function uses the 'requests' library to make an HTTP GET request to the GitHub API.
        - It uses the 'json' library to parse the JSON response from the API.
        - The function uses the 'logger' module to log messages based on the comparison results.

    Raises:
        - It may raise an exception if there's an error while making the API request or processing the response.

    """
    # Make an API request to fetch the latest version tags from the GitHub repository of RenaChan.py
    req = requests.get(f'https://api.github.com/repos/renahime/RenaChan.py/tags')
    response = json.loads(req.text)

    if req.status_code == 200:
        # If the request was successful (status code 200), check if the latest version matches the current version of the bot
        if response[0]['name'] == renachan.version():
            # If the versions match, log that the user is running the latest version.
            logger.info("You are currently running the latest version of RenaChan.py!\n")
        else:
            # If the versions don't match, check if the current version is listed in the fetched versions.
            version_listed = False
            for x in response:
                if x['name'] == renachan.version():
                    version_listed = True
                    # If the current version is listed, log that the user is not using the latest version.
                    logger.info("You are not using our latest version! :(\n")
            if not version_listed:
                # If the current version is not listed, log that the user is using an unlisted version.
                logger.info("You are currently using an unlisted version!\n")

    elif req.status_code == 404:
        # If the request returns a 404 status code, log that the latest RenaChan.py version was not found.
        logger.error("Latest RenaChan.py version not found!\n")
    elif req.status_code == 500:
        # If the request returns a 500 status code, log that there was an internal server error while fetching the latest RenaChan.py version.
        logger.error("An error occurred while fetching the latest RenaChan.py version. [500 Internal Server Error]\n")
    elif req.status_code == 502:
        # If the request returns a 502 status code, log that there was a bad gateway error while fetching the latest RenaChan.py version.
        logger.error("An error occurred while fetching the latest RenaChan.py version. [502 Bad Gateway]\n")
    elif req.status_code == 503:
        # If the request returns a 503 status code, log that the service for fetching the latest RenaChan.py version is unavailable.
        logger.error("An error occurred while fetching the latest RenaChan.py version. [503 Service Unavailable]\n")
    else:
        # If the request returns an unknown status code, log that an unknown error occurred while fetching the latest RenaChan.py version and provide the status code.
        logger.error("An unknown error has occurred when fetching the latest RenaChan.py version\n")
        logger.error("HTML Error Code:" + str(req.status_code))


def setup_bot() -> discord.ext.commands.Bot:
    """
    Sets up the Discord bot with the necessary configurations and event handlers.

    This function performs the following tasks:
        1. Sets up the intents to define which events the bot should receive from the Discord API.
        2. Creates a new discord.ext.commands.Bot instance with the specified intents and command prefix '!'.
        3. Defines an on_ready() event handler that is triggered when the bot connects to Discord and is ready to receive events.
        4. If the storage type is "sqlite", initializes the database session for the bot using renachan.managers.database.initialize_database().
        5. Initializes event handlers and command implementations from renachan.events and renachan.cogs.cmds modules.
        6. Sets the bot's presence (status and activity) on Discord using the configuration from renachan.config.bot_status().
        7. Logs the command prefix and a confirmation message indicating that the database is set, and the bot is ready to serve.

    Returns:
        discord.ext.commands.Bot: The Discord bot instance with the specified configurations and event handlers.
    """

    # Set up the intents to define which events the bot should receive from the Discord API.
    intents = discord.Intents.default()
    intents.members = True
    intents.guilds = True
    intents.typing = True
    intents.messages = True
    intents.message_content = True

    # Create a new discord.ext.commands.Bot instance with the specified intents and command prefix '!'
    bot = commands.Bot(intents=intents, command_prefix='!', help_command=None)

    # Define an on_ready() event handler that is triggered when the bot connects to Discord and is ready to receive events.
    @bot.event
    async def on_ready():
        """
        Event handler for when the bot connects to Discord and becomes ready.

        This function is automatically called by the Discord API when the bot successfully connects to Discord and is ready to start processing events.
        It is triggered only once when the bot is ready to begin handling interactions with the Discord servers.

        Note:
            - The event module contains event handlers that define how the discord bot will respond to various events, such as joining or leaving servers.
              The renachan.events.__init__(bot) call initializes these event handlers, allowing the bot to listen for and handle specific events.
            - The renachan.cogs.cmds.__init__(bot) call initializes command implementations, enabling the bot to recognize user commands and perform corresponding actions based on the inputs.
        """

        # If the storage type is "sqlite", initializes the database session for the bot.
        if renachan.config.storage_type() == "sqlite":
            bot.db = initialize_database(logger)

        # Initializes event handlers and command implementations from renachan.events and renachan.cogs.cmds modules.
        renachan.events.__init__(bot)
        renachan.cogs.cmds.__init__(bot)

        # Sets the bot's presence (status and activity) on Discord using the configuration from renachan.config.bot_status().
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(renachan.config.bot_status()))

        # Logs the command prefix and a confirmation message indicating that the database is set, and the bot is ready to serve.
        logger.info(f"{bot.command_prefix} is the command prefix")
        logger.info("Database is set, and RenaChan is on and ready to be of service :3")

    return bot  # Returns the Discord bot instance with the specified configurations and event handlers.

if __name__ == "__main__":
    """
    The conditional block that checks if the script is being run as the main program.

    If the script is being run as the main program (not imported as a module), the 'main()' function is called to start the RenaChan.py Discord bot.
    This conditional block serves as the entry point of the script.

    Explanation:
        - '__name__': A built-in variable in Python that represents the name of the current module. When a Python script is run, the value of '__name__' for that script is set to '__main__'.
        - '__main__': A special name that indicates the main program. It is the built-in value for '__name__' when the script is executed as the main program.
        - 'if __name__ == "__main__":': This conditional statement checks if the value of '__name__' is equal to "__main__", which indicates that the script is being run as the main program.
        - 'main()': The 'main()' function is called within this block to start the RenaChan.py Discord bot's execution.

    Example:
        If you run the script directly with 'python renachan.py' in the terminal, '__name__' will be '__main__', and the 'main()' function will be called, starting the bot.
        If you import the script as a module in another Python script, the '__name__' value will be set to the module name, and the 'main()' function won't be called.

    Note:
        - The 'main()' function is defined earlier in the script and is responsible for initiating the RenaChan.py Discord bot's execution.
    """
    main()
