import discord
import time
import psutil
from discord.ext import commands
from datetime import datetime

import renachan
import renachan.managers.models as models

def correct_amazon_format(ctx):
    # Access the bot instance directly from the context object
    bot = ctx.bot

    # Split the command content into individual words after the command prefix
    args = ctx.message.content[len(bot.command_prefix) + len(ctx.command.name):].split()
    print(args)
    # Check if all elements in the search are strings except the last one
    if all(isinstance(term, str) for term in args[:-1]) and args[-1].replace('.', '', 1).isdigit():
        return True
    else:
        raise commands.BadArgument("The search format is incorrect. It should be a list of strings followed by a float or an integer.")
