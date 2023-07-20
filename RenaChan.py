import os
from dotenv import load_dotenv
import time
from os.path import join, dirname
import json
import requests

from discord.ext import commands
from dotenv import load_dotenv
from renachan import *


print(f"""
Running RenaChan.py {renachan.version()}
""")


req = requests.get(f'https://api.github.com/repos/renahime/RenaChan.py/tags')
response = json.loads(req.text)

if req.status_code == 200:
    if response[0]['name'] == renachan.version():
        print("You are currently running the latest version of RenaChan.py!\n")
    else:
        version_listed = False
        for x in response:
            if x['name'] == renachan.version():
                version_listed = True
                print("You are not using our latest version! :(\n")
        if not version_listed:
            print("You are currently using an unlisted version!\n")

elif req.status_code == 404:
    # 404 Not Found
    print("Latest RenaChan.py version not found!\n")
elif req.status_code == 500:
    # 500 Internal Server Error
    print("An error occurred while fetching the latest RenaChan.py version. [500 Internal Server Error]\n")
elif req.status_code == 502:
    # 502 Bad Gateway
    print("An error occurred while fetching the latest RenaChan.py version. [502 Bad Gateway]\n")
elif req.status_code == 503:
    # 503 Service Unavailable
    print("An error occurred while fetching the latest RenaChan.py version. [503 Service Unavailable]\n")
else:
    print("An unknown error has occurred when fetching the latest RenaChan.py version\n")
    print("HTML Error Code:" + str(req.status_code))

load_dotenv(join(dirname(__file__), '.env'))

if os.getenv('CONFIG_VERSION') != renachan.config_version():
    if os.path.isfile('.env'):
        print("Missing environment variables. Please backup and delete .env, then run renachan.py again.")
        quit(2)
    print("Unable to find required environment variables. Running setup.py...")  # if .env not found
    renachan.setup.__init__() # run setup.py

print("Initializing bot...")

if renachan.config.storage_type() == "sqlite":
    db = renachan.managers.database.create_database()
    print(
        f"Database created and ready to use")


intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.typing = True
intents.messages = True
bot = commands.Bot(intents=intents, command_prefix='!', help_command=None)

@bot.event
async def on_ready():
    print(f"RenaChan is on and ready to be of service :3")
    # load cogs
    print(bot.command_prefix)
    renachan.events.__init__(bot, db)
    renachan.cogs.cmds.__init__(bot, db)
    if renachan.config.storage_type() == "sqlite":
        print("[!] Warning: This is a WIP, reach out to me if you see any errors :)")  # WIP
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(renachan.config.bot_status()))  # Update Bot status


try:
    bot.run(renachan.config.bot_token())
except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    exit(1)
