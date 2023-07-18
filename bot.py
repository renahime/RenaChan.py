import os
from dotenv import load_dotenv
import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MAX_SESSION_TIME_MINUTES = 30

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

session = Session()


@bot.event
async def on_ready():
    print("Hello! Rena-Chan is here for service u_u")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Rena-Chan is here for service u_u")

@bot.command()
async def hello(ctx):
    await ctx.send("Haiiii")

@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)
    await ctx.send(f"{result}")

@bot.command()
async def start(ctx):

    if session.is_active:
        await ctx.send("You're already studying")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    readable_time = ctx.message.created_at.strftime('%H:%M:%S')
    await ctx.send(f"Study session started at {readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("There is no study session here")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"You studied {duration} seconds this session!")

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():
    #ignoring the first iteration of the comamand
    if break_reminder.current_loop == 0:
        return

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Remember to take a break! You've been studying for {MAX_SESSION_TIME_MINUTES} minutes!")


bot.run(BOT_TOKEN)
