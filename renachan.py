import os
import sys
import requests
import json
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv
from os.path import join, dirname

from renachan import renachan
from managers.database import get_database


# Set up the logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logging.info("Running RenaChan.py v0.1")

db = None  # Define db as a global variable

# Add the parent directory of `managers` to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.typing = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!', help_command=None)

@bot.event
async def on_ready():
    global db  # Reference the global db variable
    logging.info(f"RenaChan is on and ready to be of service :3")
    # load cogs
    logging.info(f'{bot.command_prefix} is the command prefix')

    load_dotenv(join(dirname(__file__), '.env'))

    if renachan.config.storage_type() == "sqlite":
        db = get_database()  # Initialize the session

    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(renachan.config.bot_status()))  # Update Bot status

if __name__ == "__main__":
    try:
        load_dotenv(join(dirname(__file__), '.env'))
        if os.getenv('CONFIG_VERSION') != renachan.config_version():
            if os.path.isfile('.env'):
                logging.error("Missing environment variables. Please backup and delete .env, then run renachan.py again.")
                quit(2)
            logging.warning("Unable to find required environment variables. Running setup.py...")  # if .env not found
            renachan.setup.__init__()  # run setup.py

        logging.info("Initializing bot...")
        if renachan.config.storage_type() == "sqlite":
            db = get_database()  # Initialize the session

        bot.run(renachan.config.bot_token())
    except Exception as e:
        logging.error(f"[/!\\] Error: Failed to run bot!\n{e}")
        exit(1)
