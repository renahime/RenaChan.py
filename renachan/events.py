import json
import renachan
import discord
import renachan.managers.models as models
from discord.ext import commands



def __init__(bot):
    """ Initialize events """
    on_guild_join(bot)
    on_message(bot)

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

def on_message(bot):
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
    async def on_message(message):
        # ignore the message if it comes from the bot itself
        if message.author.id == bot.user.id:
            return

        # form query payload with the content of the message
        payload = {'inputs': {'text': message.content}}

        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        async with message.channel.typing():
          response = bot.query(bot, payload)
        bot_response = response.get('generated_text', None)

        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'Hmm... something is not right.'

        # send the model's response to the Discord channel
        await message.channel.send(bot_response)
