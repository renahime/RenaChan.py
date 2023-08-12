import discord
import asyncio
from discord.ext import commands
from .crawler import CreepyCrawler
import logging
import renachan
import renachan.managers.models as models
from datetime import datetime
import time as time
from .database_helpers import add_tracker, add_dm_tracker, track_time


async def send_private_message(user, message):
    """
    Sends a private message to a user.

    Parameters:
        user (discord.User): The Discord user to send the message to.
        message (str): The content of the message to send.

    Returns:
        bool: True if the message was sent successfully, False if sending the private message was forbidden.

    Explanation:
    This async function takes a target Discord user (user) and a message (message) as input.
    It attempts to send a private message to the user using the "user.send(message)" method.
    If the message is successfully sent, the function returns True. If sending the private message is forbidden,
    the function returns False.

    Note: This function is meant to be used within an asynchronous context, as it uses the "async" keyword for asynchronous
    operations with Discord API calls (e.g., sending private messages).

    Example Usage:
        user = bot.get_user(1234567890)  # Replace 1234567890 with the user ID you want to message.
        if user:
            result = await send_private_message(user, "Hello! This is a private message.")
            if result:
                print("Private message sent successfully.")
            else:
                print("Failed to send the private message.")
    """
    try:
        # Attempt to send the message to the user privately
        await user.send(message)
        return True
    except discord.Forbidden:
        return False

async def ping_user_in_server_channel(bot, user, message):
    """
    Pings a user in the first available general text channel of a server where both the bot and user are present.

    Parameters:
        bot (discord.Client): The Discord bot client instance.
        user (discord.User): The Discord user to ping.
        message (str): The message to send along with the user mention.

    Returns:
        discord.TextChannel or None: The general text channel where the user was pinged, or None if no suitable channel was found.

    Explanation:
    This async function takes the Discord bot client (bot), a target user, and a message as input.
    It then attempts to find the first available general text channel in any of the bot's connected guilds (servers)
    where both the bot and the user are present as members. Once the general text channel is found, it pings the user
    by mentioning them in the channel with the provided message.

    The function works as follows:

    1. Iterate through each guild (server) in which the bot is present.
    2. Check if the target user (user) is a member of the current guild using "user in guild.members".
    3. If the user is a member of the guild, attempt to find the "general" text channel in that guild using
       discord.utils.get(guild.text_channels, name="general").
    4. If a suitable general text channel is found (general_channel is not None), ping the user by mentioning them with
       their user ID (mention = user.mention) and send the provided message along with the mention.
    5. After sending the message, return the general text channel where the user was pinged.
    6. If no suitable general text channel is found in any of the guilds where both the bot and the user are members,
       return None.

    Note: This function is meant to be used within an asynchronous context, as it uses the "async" keyword for asynchronous
    operations with Discord API calls (e.g., sending messages).
    """
    for guild in bot.guilds:
        if user in guild.members:
            general_channel = discord.utils.get(guild.text_channels, name="general")
            if general_channel:
                # If a general channel is found, ping the user in that channel
                mention = user.mention
                await general_channel.send(f"{mention}, {message}")
                return general_channel
    return None

async def ping_user_in_text_channel(bot, user, message):
    """
    Pings a user in the first available text channel where the bot has permissions to send messages.

    Parameters:
        bot (discord.Client): The Discord bot client instance.
        user (discord.User): The Discord user to ping.
        message (str): The message to send along with the user mention.

    Returns:
        discord.TextChannel or None: The text channel where the user was pinged, or None if no suitable channel was found.

    Explanation:
    This async function takes the Discord bot client (bot), a target user, and a message as input.
    It then attempts to find the first available text channel in any of the bot's connected guilds where the bot has
    permissions to send messages. Once the text channel is found, it pings the user by mentioning them in the channel
    with the provided message.

    The function works as follows:

    1. Iterate through each guild (server) in which the bot is present.
    2. Use the discord.utils.get() function to find the first available text channel in the guild. The bot checks for
       the necessary permissions to send messages in each channel.
    3. If a suitable text channel is found (text_channel is not None), ping the user by mentioning them with their user ID
       (mention = user.mention) and send the provided message along with the mention.
    4. After sending the message, return the text channel where the user was pinged.
    5. If no suitable text channel is found in any of the guilds, return None.

    Note: This function is meant to be used within an asynchronous context, as it uses the "async" keyword for asynchronous
    operations with Discord API calls (e.g., sending messages).
    """
    for guild in bot.guilds:
        text_channel = discord.utils.get(guild.text_channels)
        if text_channel:
            # If a text channel is found, ping the user in that channel
            mention = user.mention
            await text_channel.send(f"{mention}, {message}")
            return text_channel
    return None


async def send_message(bot, user, channel, message):
    """
    Send a message to a user through private messages or ping them in a server channel.

    Parameters:
        bot (discord.Client): The Discord bot instance.
        user (discord.User): The user to whom the message will be sent.
        channel (discord.TextChannel or discord.DMChannel): The channel from which the function was called.
        message (str): The content of the message to be sent.

    This function attempts to send the `message` to the specified `user` privately. If the bot does not have permission
    to send direct messages to the user, it will ping them in the server's general channel or any available text channel
    where it has permissions to send messages.

    If the bot successfully sends the message privately, it sends a confirmation message in the original channel
    to indicate that the message has been sent privately to the user in the specific server (if applicable).

    If the bot cannot send the message privately and cannot find a suitable channel to ping the user, it will send a message
    in the original channel to inform the user about the issue.

    Note:
        This function uses the discord.utils.get() method to find the general channel or any available text channel.
        If the server has no "general" channel and no available text channels, the bot will not be able to send any messages.
        Make sure the bot has the necessary permissions to send messages in the server and access to the "general" channel (if applicable).

    Example usage:
        await send_message(bot, user, channel, "Hello, this is a private message!")
    """
    if await send_private_message(user, message):
        # Send a confirmation message in the original channel to indicate the message was sent privately
        await channel.send(f"Message sent to {user.name} privately in server '{user.guild.name}'.")
    else:
        # Try to ping the user in a server channel
        server_channel = await ping_user_in_server_channel(bot, user, message)
        if server_channel:
            await channel.send(f"I couldn't privately message {user.name}, so I pinged them in server '{user.guild.name}' in the general channel.")
        else:
            # Try to ping the user in a text channel
            text_channel = await ping_user_in_text_channel(bot, user, message)
            if text_channel:
                await channel.send(f"I couldn't privately message {user.name} or find a shared server, so I pinged them in text channel '{text_channel.name}' in server '{text_channel.guild.name}'.")
            else:
                # If no suitable channel is found, send a message in the original channel to inform the user about the issue
                await channel.send(f"The server '{user.guild.name}' doesn't have a 'general' channel, and I couldn't find any available text channels.")


def in_dm():
    """
    A custom check decorator that checks if the command is coming from a direct message.

    Returns:
        A check function that raises a `commands.CheckFailure` error if the command is not coming from a DM.
    """
    async def predicate(ctx):
        """
        The actual check function that checks if the command is coming from a direct message.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            bool: True if the command is coming from a DM, or raises a `commands.CheckFailure` error otherwise.
        """
        if ctx.guild is None:
            return True
        else:
            general_channel = discord.utils.get(ctx.guild.channels, name="general")
            if general_channel:
                await general_channel.send("This totally defeats the purpose of this command!!!!")
            else:
                raise commands.CheckFailure("This command can only be used in a direct message (DM).")
    return commands.check(predicate)

async def start_crawl(ctx, bot, command_data):
    try:
        time_start = time.time()
        data = {'user_id': ctx.author.id, 'username': ctx.author.name, 'command':ctx.message.content}
        crawler = CreepyCrawler(url=command_data["url"])

        ## Grabbing html tags that share this class
        if "class" in command_data['type']:
            possible_results = crawler.crawler_by_item_class(class_name=command_data['start'])

        possible_results = crawler.crawler_by_item_id(item_id=command_data['start'])

        ## Log Error
        if not possible_results:
            await ctx.send(f"Sowwi couldn't find what you were looking for :c")
            time_end = time.time()
            data['last_response'] = "error: unable to find html tag"
            data['duration'] = time_end - time_start
            await track_time(ctx, bot, data)

        ## Finding correct item
        correct_element = crawler.find_correct_element(possible_results, command_data['title'], ctx)

        ## Log Error
        if not correct_element:
            await ctx.send(f"Sowwi I couldn't find the right price :c")
            time_end = time.time()
            data['last_response'] = "error: unable to find price"
            data['duration'] = time_end - time_start
            await track_time(ctx, bot, data)

        await ctx.send(f"Parsing Price")
        price = crawler.extract_number_from_class(possible_results[0], currency=command_data['currency_symbol'])
        await add_tracker(ctx,bot,command_data['title'],command_data['url'],price=price)
        time_end = time.time()
        data['last_response'] = "success"
        data['duration'] = time_end - time_start
        await track_time(ctx, data, bot)

    except Exception as e:
        print(e)
        await ctx.send(str(e))

async def ai_chat(bot, message):
    # Ignore the message if it comes from the bot itself
    if message.author.id == bot.user.id:
        return

    # Form query payload with the content of the message
    payload = {'inputs': {'text': message.content}}

    # While the bot is waiting on a response from the model,
    # set its status as typing for user-friendliness
    async with message.channel.typing():
        response = bot.query(bot, payload)

    bot_response = response.get('generated_text', None)

    # We may get an ill-formed response if the model hasn't fully loaded
    # or has timed out
    if not bot_response:
        if 'error' in response:
            bot_response = '`Error: {}`'.format(response['error'])
        else:
            bot_response = 'Hmm... something is not right.'

    # Send the model's response to the Discord channel
    await message.channel.send(bot_response)
