import renachan.managers.models as models
import renachan
from datetime import time


def add_to_database(bot, item):
     bot.db.add(item)
     bot.db.commit()
     bot.db.close()

def check_membership(bot, ctx):
    member = bot.db.query(models.Member).filter_by(id=ctx.author.guild.id).first()

    if member:
         return member

    new_member = models.Member(
            id=ctx.author.id,
            username=ctx.author.name
        )

    add_to_database(bot, new_member)

    return new_member

def create_tracker(bot, ctx, title, url, price, member):
     if ctx.guild:
        server = bot.db.query(models.Server).filter_by(id=ctx.guild.id).first()
        server_tracker = models.Tracker(
            track_url=url,
            title=title,
            available=True,  # Set initial values as necessary
            price=price,      # Set initial values as necessary
            member=member,  # Set the member relationship
            server=server   # Set the server relationship
        )
        return server_tracker

     member_tracker = models.Tracker(
        track_url=url,
        title=title,
        available=True,  # Set initial values as necessary
        price=price,      # Set initial values as necessary
        member=member,  # Set the member relationship
        )

     return member_tracker


async def add_tracker(ctx, bot, title, url, price):
    member = check_membership()

    await ctx.send(f"""I found the {title} you want!\nChecking the database now... \nWIP: Getting availability, adding tasks/stat queries to make requests to check prices""")

    existing_tracker = bot.db.query(renachan.models.Tracker).filter_by(member_id=ctx.author.id, track_url=url).first()

    if not existing_tracker:
        tracker = create_tracker(bot, ctx, title, url, price, member)
        add_to_database(bot, tracker)
        await ctx.send(f"Success! I added it to the database. Will update you if the price changes or it goes out of stock :3")
    else:
        await ctx.send(f"I am already tracking this on the database. Stat queries are curretly a WIP!")


async def track_time(ctx, bot, data):
    new_bot_command = models.BotCommands(
         user_id=data['user_id'],
         username=data['username'],
         command=data['command'],
         last_response=data['last_response'],
         duration=data['duration']
    )
    add_to_database(bot, new_bot_command)
    if "error" in data['last_response']:
         await ctx.send(f"sorry you got an error :( feel free to suggest any input on how to make renachan.py better :) this command took {data['duration']} ms to complete thanks so much for checking my bot out :)")
    else:
         await ctx.send(f"thanks so much for checking my discord bot out! this command took {data['duration']} ms to complete")
