import json
import renachan
import discord
import renachan.managers.models as models


def __init__(bot):
    """ Initialize events """
    on_guild_join(bot)

def on_guild_join(bot):
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
