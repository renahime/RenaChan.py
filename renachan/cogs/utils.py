import discord
import asyncio
from discord.ext import commands

async def send_message(user, channel, message):
    """
    Send a message to a user through private messages or ping them in a server channel.

    Parameters:
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
        await send_message(user, channel, "Hello, this is a private message!")
    """
    try:
        # Attempt to send the message to the user privately
        await user.send(message)
        # Send a confirmation message in the original channel to indicate the message was sent privately
        await channel.send(f"Message sent to {user.name} privately in server '{user.guild.name}'.")
    except discord.Forbidden:
        # If bot cannot privately message the user, try to ping them in the server's general channel or any available text channel
        general_channel = discord.utils.get(user.guild.channels, name="general")
        if not general_channel:
            # If there is no "general" channel, use the first available text channel
            general_channel = discord.utils.get(user.guild.text_channels)

        if general_channel:
            # If a general channel or text channel is found, ping the user in that channel
            mention = user.mention
            await general_channel.send(f"{mention}, {message}")
            # Send a message in the original channel to inform the user that they were pinged in the specified channel
            await channel.send(f"I couldn't privately message {user.name}, so I pinged them in server '{user.guild.name}' in the general channel.")
        else:
            # If no suitable channel is found, send a message in the original channel to inform the user about the issue
            await channel.send(f"The server '{user.guild.name}' doesn't have a 'general' channel, and I couldn't find any available text channels.")
