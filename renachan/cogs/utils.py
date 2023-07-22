import discord
import asyncio
from discord.ext import commands
import logging

async def send_private_message(user, message):
    try:
        # Attempt to send the message to the user privately
        await user.send(message)
        return True
    except discord.Forbidden:
        return False

async def ping_user_in_server_channel(bot, user, message):
    # Try to find a general channel in a server that both the bot and user share
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
    # Try to find the first available text channel where the bot has permissions to send messages
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
