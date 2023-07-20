import json
import renachan
import discord


def __init__(bot, db):
    """ Initialize events """
    on_guild_join(bot, db)
    # on_command_error(bot)


# def join(bot, db):
#     @bot.event
#     async def on_member_join(member):
#         if renachan.config.storage_type() == "sqlite":
#             new_member = renachan.database.User()
#             try:
#                 db.execute(
#                     "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s)",
#                     (renachan.time(), member.guild.id, member.channel.id, member.id, "MEMBER_JOIN"))
#                 db.commit()
#             except Exception as e:
#                 print(e)


# def leave(bot, session):
#     @bot.event
#     async def on_member_remove(member):
#         if renachan.config.storage_type() == "mysql":
#             try:
#                 db.execute(
#                     "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s)",
#                     (renachan.time(), member.guild.id, member.channel.id, member.id, "MEMBER_REMOVE"))
#                 database.commit()
#             except Exception as e:
#                 print(e)


def on_guild_join(bot, db):
    @bot.event
    async def on_guild_join(guild):
        if renachan.config.storage_type() == "sqlite":
            # Finding general text channel to send the welcome message
            server_id = guild.id
            owner_id = guild.owner_id
            server_name = guild.name
            owner_username = guild.owner.name
            owner= renachan.database.Owner(id=owner_id, username=owner_username)
            server = renachan.database.Server(id=server_id,server_name=server_name, user=owner)
            general_channel = next((channel for channel in guild.text_channels if channel.name.lower() == 'general'), None)
            for member in guild.members:
                user = renachan.database.Member(id=member.id, name=member.name)
                db.add(user)

            # Log all channels in the server
            for channel in guild.channels:
                channel = renachan.database.Channel(id=channel.id, name=channel.name)
                db.add(channel)

            db.commit()
            db.close()
            if channel:
                welcome_message = "Rena-Chan has arrivied and is ready to service :3"
                await channel.send(general_channel)
            else:
                return
