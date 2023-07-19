import os
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


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

req = requests.get(f'https://api.github.com/repos/renahime/RenaChan.py/tags')
response = json.loads(req.text)

print(response)
print(req.status_code)

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




# @bot.event
# async def on_ready():
#     print("Hello! Rena-Chan is here for service u_u")
#     channel = bot.get_channel(CHANNEL_ID)
#     await channel.send("Hello! Rena-Chan is here for service u_u")

# bot.run(BOT_TOKEN)
