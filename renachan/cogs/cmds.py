import discord
import time
import psutil
from discord.ext import commands as cmd
from .utils import *

import renachan

def __init__(bot):
    """
    Initialize commands for the bot.

    Parameters:
        bot (discord.ext.commands.Bot): The instance of the Discord bot.

    This function initializes the custom commands for the bot. It calls other functions to create and define individual commands,
    allowing the bot to respond to different user inputs or perform specific actions.

    Note:
        - Custom commands are defined using separate functions for better code organization.
        - In this implementation, the `hello` and `harass` commands are initialized.

    Example usage:
        # Initialize commands for the bot instance 'bot'
        __init__(bot)
    """
    # Initialize individual commands for the bot instance 'bot'
    hello(bot)   # Create the 'hello' command that sends a simple greeting message.
    harass(bot)  # Create the 'harass' command that allows the bot to send continuous messages to a user.


def hello(bot):
    """
    Create a 'hello' command for the bot.

    Parameters:
        bot (discord.ext.commands.Bot): The instance of the Discord bot.

    This function defines a 'hello' command that allows the bot to respond with a simple greeting message when the command is invoked.

    Parameters for the 'hello' command:
        - ctx (discord.ext.commands.Context): The context of the command, containing information about the invocation.

    Note:
        - The 'hello' command does not take any additional parameters. It simply sends a fixed greeting message when invoked.
        - The bot must have the necessary permissions to send messages in the channel where the command is used.

    Example usage of the 'hello' command:
        !hello

    Output:
        The bot responds with "Haiiii".
    """
    @bot.command()
    async def hello(ctx):
        # Send a simple greeting message to the channel where the command was invoked
        await ctx.send("Haiiii")


def harass(bot):
    """
    Create a 'harass' command for the bot.

    Parameters:
        bot (discord.ext.commands.Bot): The instance of the Discord bot.

    This function defines a 'harass' command that allows the bot to send continuous messages to a user, either privately
    or by pinging them in a server channel, while respecting the Discord rate limit.

    Parameters for the 'harass' command:
        - username (str): The username of the user to harass.
        - password (str): The password that the user needs to respond with to stop the harassment.
        - message (str): The content of the message to send in the harassment.

    Note:
        - The bot must have the necessary permissions to send messages in the server and access to the "general" channel (if applicable).
        - The 'harass' command utilizes the `send_message` function, which handles the message sending logic.

    Example usage of the 'harass' command:
        !harass JohnDoe mysecretpassword Hello, this is a harassment message!
    """
    @bot.command()
    async def harass(ctx, username: str, *, password: str, message: str):
        # Find the user in any of the bot's guilds (servers)
        user = None
        for guild in bot.guilds:
            user = discord.utils.get(guild.members, name=username)
            if user:
                break

        if user:
            # Send the initial message to the user
            await send_message(user, ctx.channel, message)

            # Continuously send the message respecting the rate limit
            while True:
                await asyncio.sleep(5)

                # Check if the user has responded with the correct password
                async for response in bot.wait_for('message', check=lambda m: m.author == user):
                    if response.content.strip() == password:
                        # Stop harassment if the user provided the correct password
                        await ctx.send(f"Messages to {user.name} have been stopped.")
                        return

                # Send the message again
                await send_message(user, ctx.channel, message)
        else:
            # If the user was not found in any server where the bot is a member
            await ctx.send(f"{username} was not found in any server where I am a member.")



######################### WIP
# Note: These are functions used in a discord bot tutorial I followed, I will be implementing these to work with my bot in the near future...
#
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
