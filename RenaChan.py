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

@bot.event
async def on_ready():
    print("Hello! Rena-Chan is here for service u_u")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Rena-Chan is here for service u_u")

bot.run(BOT_TOKEN)
