import discord
import time
import psutil
from discord.ext import commands as cmd
from .utils.discord_helpers import *
from .utils.command_checks import *
from datetime import datetime

import renachan
import renachan.managers.models as models

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
    setup_harass_command(bot)  # Create the 'harass' command that allows the bot to send continuous messages to a user.
    setup_track_command(bot) # Create the 'track' command that allows the bot to track an item the user is interested in


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


def setup_harass_command(bot):
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
        - The 'harass' command can only be used in a direct message (DM) with the bot.

    Example usage of the 'harass' command:
        !harass JohnDoe mysecretpassword Hello, this is a harassment message!
    """
    @bot.command()
    @in_dm()  # Use the custom check decorator to ensure the command is coming from a DM
    async def harass(ctx, *, input_list: str):
        # Split the input_list into individual components
        params = input_list.split()
        if len(params) != 3:
            await ctx.send("Invalid number of parameters. The command should be: !harass username password message")
            return

        # Extract individual components
        username, password, message = params

        # Find the user in any of the bot's guilds (servers)
        user = None
        for guild in bot.guilds:
            user = discord.utils.get(guild.members, name=username)
            if user:
                await ctx.send(f"Found {username}, I'm off to annoying them now...")
                break
        if user:
            # Send the initial message to the user
            await send_message(bot, user, ctx.channel, message)
            # Continuously send the message respecting the rate limit
            while True:
                try:
                    response = await bot.wait_for('message', timeout=5, check=lambda m: m.author == user)
                except asyncio.TimeoutError:
                    # If the wait times out, send the message again
                    await send_message(bot, user, ctx.channel, message)
                else:
                    if response.content.strip() == password:
                        # Stop harassment if the user provided the correct password
                        await ctx.send(f"I have stopped annoying {username}")
                        return
        else:
            # If the user was not found in any server where the bot is a member
            await ctx.send(f"{username} was not found in any server where I am a member.")

def setup_track_command(bot):
    """
    Discord bot command to track an item's price and availability using web crawling.

    Parameters:
        ctx (discord.ext.commands.Context): The Discord command context.
        url (str): The URL of the web page to crawl for the item's information.
        item_id (str): The 'id' attribute value of the HTML element that contains the item's price.
        currency_symbol (str): The currency symbol used to represent the price.

    Returns:
        None

    Explanation:
    This function is a Discord bot command to track an item's price and availability using web crawling.
    It takes a Discord command context (ctx), the URL of the web page to crawl (url), the 'id' attribute value of the HTML
    element that contains the item's price (item_id), and the currency symbol used to represent the price (currency_symbol).

    The function attempts to find an embed in the command message and extracts the title from it.

    It then calls the crawler_by_item_id() function to crawl the web page, extract the item's price, and parse it as a floating-point value.

    If a single price is found, the function creates a new tracker entry in the database with the item's information and the author's
    (member) and server's (guild) relationships. It sets the availability as True, the initial price, and the current timestamp
    as the last_checked value.

    Finally, the function adds the new tracker entry to the database and commits the changes. The bot responds to the user with
    appropriate messages about the tracking process.

    If more than one price is found, the bot informs the user that it currently does not support tracking items with multiple prices.

    Note: The function uses a database model (models.Tracker) to store the tracked item's information in the database.

    Example Usage:
        !track https://example.com/item123 price_element $  # The bot will attempt to track the item's price from the provided URL and HTML element ID.
    """
    @bot.command()
    async def track(ctx, type:str, url: str, start: str, currency_symbol: str):
        await ctx.send(f"Testing finding {type}, {url}, {start}, {currency_symbol}")
        title = None  # Initialize 'title' with a default value
        # Check if the command message has any embeds
        if ctx.message.embeds:

            embed = ctx.message.embeds[0]
            title = embed.title
            description = embed.description


        if type == "id":
            await ctx.send(f"Creepy crawling the web... :3")
            await start_at_id(ctx, bot, url, title, start, currency_symbol)
        else:
            type == "class"
            await start_at_class(ctx, bot, url, title, start, currency_symbol)









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
