import json
import renachan
import discord
import renachan.managers.models as models
from discord.ext import commands



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
def on_guild_join(bot):
    """
    This function is called when the bot joins a new guild (server). It performs the following tasks:
    1. Extracts guild information, such as server ID, owner ID, server name, and owner username.
    2. Checks if the owner already exists in the database and adds it if not.
    3. Adds the new server to the database.
    4. Associates guild members with the server in the database, will include new members to the database if they are not there.
    5. Finds the 'general' channel in the guild and sends a welcome message there or in the first text channel.

    Parameters:
        guild (discord.Guild): The Discord guild (server) that the bot has joined.

    Notes:
        - This function assumes that 'renachan.config' and 'renachan.models' have been imported and properly set up.
        - The function relies on a database session named 'bot.db' to perform database operations.
        - It is assumed that 'bot' is an instance of the bot (client) used to interact with Discord.

    """
    @bot.event
    async def on_guild_join(guild):
        if renachan.config.storage_type() == "sqlite":
            server_id = guild.id
            owner_id = guild.owner_id
            server_name = guild.name
            owner_username = guild.owner.name

            # Check if the owner already exists in the database
            existing_owner = bot.db.query(renachan.models.Owner).filter_by(id=owner_id).first()

            # If the owner does not exist, add it to the database
            if not existing_owner:
                owner = renachan.models.Owner(id=owner_id, username=owner_username)
                bot.db.add(owner)

            # Add the new server to the database
            server = renachan.models.Server(id=server_id, server_name=server_name, owner=existing_owner)
            bot.db.add(server)

            # Commit the changes to the database
            bot.db.commit()

            # Iterate through the guild members and associate them with the server
            for member in guild.members:
                member_id = member.id
                member_username = member.name
                member_discriminator = member.discriminator

                # Check if the member already exists in the database
                existing_member = bot.db.query(renachan.models.Member).filter_by(id=member_id).first()
                if existing_member:
                    # If the member exists, retrieve the member instance and add the server to its 'servers' relationship
                    existing_member.servers.append(server)
                else:
                    # If the member does not exist, create a new member instance and add it to the database with the associated server
                    new_member = renachan.models.Member(id=member_id, username=member_username, user_discriminator=member_discriminator)
                    new_member.servers.append(server)
                    bot.db.add(new_member)

            # Finding General Channel
            general_channel = next((channel for channel in guild.text_channels if channel.name == 'general'), None)

            # Commit the changes to the database and close the session
            bot.db.commit()
            bot.db.close()

            # Send the welcome message if the 'general' channel is found
            if general_channel:
                welcome_message = "Rena-Chan has arrived and is ready to serve! :3"
                await general_channel.send(welcome_message)
            else:
                # If 'general' channel doesn't exist, send it to the first text channel in the guild
                first_text_channel = next((channel for channel in guild.text_channels), None)
                if first_text_channel:
                    await first_text_channel.send(welcome_message)

def on_guild_join(bot):
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(str(error))
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid command. Please check the command syntax.")
        else:
            await ctx.send("An error occurred while executing the command.")
