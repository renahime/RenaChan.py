import json
import renachan
import discord
import renachan.managers.models as models


def __init__(bot):
    """ Initialize events """
    on_guild_join(bot)

def on_guild_join(bot):
    """
    Event handler for when the bot joins a new guild (server).

    Parameters:
        bot (discord.ext.commands.Bot): The instance of the Discord bot.

    This function defines the behavior of the bot when it joins a new guild (server). It handles tasks such as sending a welcome message
    to the 'general' channel (if available) or the first available text channel in the server. It also collects and stores information
    about the server, its owner, members, and channels in the SQLite database (if applicable).

    Note:
        - The 'on_guild_join' event is automatically triggered by Discord when the bot joins a new server.
        - The function uses the renachan.config.storage_type() function to check if the bot is using SQLite as its storage type.
        - The function accesses information about the new guild, such as its ID, name, owner ID, and owner username, to store them in the database.
        - It creates instances of the renachan.models.Owner and renachan.models.Server classes to represent the owner and server, respectively.
        - For each member in the guild, the function creates an instance of the renachan.models.Member class to represent the member and their associated servers.
        - For each channel in the guild, the function creates an instance of the renachan.models.Channel class to represent the channel and its associated server.
        - The function uses bot.db to interact with the SQLite database. The data is committed and the session is closed after adding the information.
        - If the 'general' channel exists in the server, the bot sends a welcome message to it. Otherwise, it sends the message to the first available text channel.
    """
    @bot.event
    async def on_guild_join(guild):
        if renachan.config.storage_type() == "sqlite":
            # Finding general text channel to send the welcome message
            server_id = guild.id
            owner_id = guild.owner_id
            server_name = guild.name
            owner_username = guild.owner.name
            # Collecting Owner Info
            owner = renachan.models.Owner(id=owner_id, username=owner_username)
            # Collecting Server Info
            server = renachan.models.Server(id=server_id, server_name=server_name, owner=owner)
            # Finding General Channel
            general_channel = next((channel for channel in guild.text_channels if channel.name == 'general'), None)
            # Collecting Member Info
            for member in guild.members:
                member = renachan.models.Member(id=member.id, username=member.name, servers=[server])
                bot.db.add(member)

            # Collecting Channel
            for channel in guild.channels:
                channel_data = renachan.models.Channel(id=channel.id, channel_name=channel.name, server=server)
                bot.db.add(channel_data)
            # Ending db session
            bot.db.commit()
            bot.db.close()
            # If the 'general' channel is found then it will send it to the general channel.
            if general_channel:
                welcome_message = "Rena-Chan has arrived and is ready to serve! :3"
                await general_channel.send(welcome_message)
            else:
                # If 'general' channel doesn't exist send it to the first text channel in the guild:
                first_text_channel = next((channel for channel in guild.text_channels), None)
                if first_text_channel:
                    await first_text_channel.send(welcome_message)
