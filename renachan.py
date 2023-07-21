### The bot script by setting up imports and the logging configuration. This ensures that necessary libraries and modules are available and sets up a basic logging system to track events
### in the bot's execution.
import os
import sys
import requests
import json
import logging

### os, sys, requests, json, logging: These are standard Python libraries that provide various functionalities for handling operating system tasks, making HTTP requests,
### working with JSON data, and logging.

import discord
from discord.ext import commands
### discord, discord.ext.commands: These are part of the Discord.py library, which allows interaction with the Discord API and simplifies creating a Discord bot.

from dotenv import load_dotenv
from os.path import join, dirname
### dotenv: This library loads environment variables from a .env file into the bot's runtime environment.


# Set up the logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logging.info("Running RenaChan.py v0.1")

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(join(dirname(__file__), '.env'))

from renachan import renachan  # Import renachan package
from renachan.managers.database import initialize_database

### renachan: A package is a way to organize Python modules in a directory. It is a collection of Python modules and may contain a __init__.py file (not to be confused with the .env file).
### The package here contains the main functionality of the bot, and the renachan module inside this package is imported for use in the script.

### renachan.managers.database: This is a module within the renachan package responsible for managing the bot's database.
### The initialize_database() function from this module will be used later to initialize the database.

### This part of the script makes an API request to the GitHub repository to get the latest version tag of RenaChan.py.
### requests.get(): This function is used to perform an HTTP GET request to the specified URL.
### The GitHub tags represent versions or milestones of the repository. A new tag is created for each version release or significant update.
### If the request returns a status code of 200 (OK), it checks whether the fetched version matches the current version of the bot (renachan.version()).
### If it matches, it logs that the bot is running the latest version. If not, it logs whether the version is unlisted or not the latest.
req = requests.get(f'https://api.github.com/repos/renahime/RenaChan.py/tags')
response = json.loads(req.text)

if req.status_code == 200:
    if response[0]['name'] == renachan.version():
        logging.info("You are currently running the latest version of RenaChan.py!\n")
    else:
        version_listed = False
        for x in response:
            if x['name'] == renachan.version():
                version_listed = True
                logging.info("You are not using our latest version! :(\n")
        if not version_listed:
            logging.info("You are currently using an unlisted version!\n")

elif req.status_code == 404:
    # 404 Not Found
    logging.error("Latest RenaChan.py version not found!\n")
elif req.status_code == 500:
    # 500 Internal Server Error
    logging.error("An error occurred while fetching the latest RenaChan.py version. [500 Internal Server Error]\n")
elif req.status_code == 502:
    # 502 Bad Gateway
    logging.error("An error occurred while fetching the latest RenaChan.py version. [502 Bad Gateway]\n")
elif req.status_code == 503:
    # 503 Service Unavailable
    logging.error("An error occurred while fetching the latest RenaChan.py version. [503 Service Unavailable]\n")
else:
    logging.error("An unknown error has occurred when fetching the latest RenaChan.py version\n")
    logging.error("HTML Error Code:" + str(req.status_code))

### This part of the script creates the discord bot
### Here, we create a new discord.Bot instance with specific intents.
### discord.Intents: Discord.py allows you to define which events you want to receive from the Discord API.
### In this case, the bot requires access to member-related events, guilds, typing events, messages, and message content.
### The discord.Intents.default() function creates a set of default intents.
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.typing = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!', help_command=None)


### The on_ready() function is an event in Discord.py that is triggered when the bot connects to Discord and is ready to start receiving events.
### If the storage type is "sqlite", the function initialize_database() from the renachan.managers.database module is called to initialize the database session for the bot.
### renachan.events and renachan.cogs.cmds: These are modules within the renachan package that contain event handling and command implementations, respectively. The bot initializes these modules to handle events and commands.
### bot.change_presence(): This sets the bot's presence on Discord, such as its status and activity (playing a game, streaming, etc.).


# The on_ready() function is called when the bot is ready to start receiving events from Discord.
@bot.event
async def on_ready():
    # Initialize the database if the storage type is "sqlite"
    ### renachan.config.storage_type(): This function from the renachan package returns the type of storage used for the bot's data (e.g., SQLite, MySQL, etc.).
    if renachan.config.storage_type() == "sqlite":
        # The session object that SQLAlchemy returns gets assigned to the bot so that we don't need to pass it over to our package/modules
        bot.db = initialize_database()

    ### Load event handling and command implementations
    ### The event module contains event handlers that when defined the discord bot will trigger anytime there is an event that needs to be preformed.
    ### eg. The bot joining a server, someone leaving the server... ext
    renachan.events.__init__(bot)
    ### The cmds module is responsible for holding all the commands the discord bot knows
    ### so when a user in a server uses the prefix and correct command the bot will recognize it and perform an action
    renachan.cogs.cmds.__init__(bot)
    ## This step is crucial for the bot to properly listen for and respond to various Discord events and execute custom commands based on user inputs.

    # Set the bot's status on Discord
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(renachan.config.bot_status()))

    logging.info(f"{bot.command_prefix} is the command prefix")
    logging.info("Database is set, and RenaChan is on and ready to be of service :3")


### This part is the entry point of the script, where the bot execution begins.
### The condition if __name__ == "__main__": ensures that this block is only executed when the script is run as the main program, not when it is imported as a module.
### The block checks if the current CONFIG_VERSION environment variable matches the one stored in the renachan package (renachan.config_version()). If not, it checks if the .env file exists. If it does, it means that the required environment variables are missing, and it logs an error message instructing the user to run renachan.py again after setting up the environment variables using setup.py.
### If the .env file doesn't exist, it means the setup needs to be performed. The script initializes the setup process using renachan.setup.__init__().
### If everything is set up correctly, the bot is initialized with bot.run(renachan.config.bot_token()).

if __name__ == "__main__":
    try:
        # Check if CONFIG_VERSION matches the one stored in the package
        if os.getenv('CONFIG_VERSION') != renachan.config_version():
            # Check if .env file exists
            if os.path.isfile('.env'):
                logging.error("Missing environment variables. Please backup and delete .env, then run renachan.py again.")
                quit(2)

            logging.warning("Unable to find required environment variables. Running setup.py...")
            renachan.setup.__init__()  # run setup.py

        logging.info("Initializing bot...")
        bot.run(renachan.config.bot_token())
    except Exception as e:
        logging.error(f"[/!\\] Error: Failed to run bot!\n{e}")
        exit(1)
