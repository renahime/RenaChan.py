import discord
import time
import psutil
from discord.ext import commands as cmd

import renachan

MAX_SESSION_TIME_MINUTES = 30

def __init__(bot):
    """ Initialize commands """
    hello(bot)
    # add(bot)
    # start(bot, session)
    # end(bot, session)


def hello(bot):
  @bot.command()
  async def hello(ctx):
      await ctx.send("Haiiii")

# def add(bot):
#   @bot.command()
#   async def add(ctx, *arr):
#       result = 0
#       for i in arr:
#           result += int(i)
#       await ctx.send(f"{result}")

# def start(bot, session):
#   @bot.command()
#   async def start(ctx):

#       if session.is_active:
#           await ctx.send("You're already studying")
#           return

#       session.is_active = True
#       session.start_time = ctx.message.created_at.timestamp()
#       readable_time = ctx.message.created_at.strftime('%H:%M:%S')
#       await ctx.send(f"Study session started at {readable_time}")

# def end(bot, session):
#     @bot.command()
#     async def end(ctx):
#         if not session.is_active:
#             await ctx.send("There is no study session here")
#             return

#         session.is_active = False
#         end_time = ctx.message.created_at.timestamp()
#         duration = end_time - session.start_time
#         human_readable = str(datetime.timedelta(seconds=duration))
#         break_reminder.stop()
#         await ctx.send(f"You studied {duration} seconds this session!")

# def start_reminder(bot):
#     @tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
#     async def break_reminder():
#         #ignoring the first iteration of the comamand
#         if break_reminder.current_loop == 0:
#             return
#         channel = bot.get_channel(CHANNEL_ID)
#         await channel.send(f"Remember to take a break! You've been studying for {MAX_SESSION_TIME_MINUTES} minutes!")
