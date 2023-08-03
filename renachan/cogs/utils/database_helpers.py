import renachan.managers.models as models
import renachan
from datetime import time

async def add_tracker(ctx, bot, title, url, price):
    member = bot.db.query(models.Member).filter_by(id=ctx.author.id).first()
    server = bot.db.query(models.Server).filter_by(id=ctx.guild.id).first()
    await ctx.send(f"""I found the {title} you want!\nChecking the database now... \nWIP: Getting availability, adding tasks/stat queries to make requests to check prices""")
    existing_tracker = bot.db.query(renachan.models.Tracker).filter_by(member_id=ctx.author.id, track_url=url).first()
    if not existing_tracker:
        new_tracker = models.Tracker(
            track_url=url,
            title=title,
            available=True,  # Set initial values as necessary
            price=price,      # Set initial values as necessary
            member=member,  # Set the member relationship
            server=server   # Set the server relationship
        )
        bot.db.add(new_tracker)
        bot.db.commit()
        await ctx.send(f"Success! I added it to the database. Will update you if the price changes or it goes out of stock :3")
    else:
        await ctx.send(f"I am already tracking this on the database. Stat queries are curretly a WIP!")

async def add_dm_tracker(ctx,bot,title,url,price):
    member = bot.db.query(models.Member).filter_by(id=ctx.author.id).first()
    existing_tracker = bot.db.query(renachan.models.Tracker).filter_by(member_id=ctx.author.id, track_url=url).first()
    if not member:
        new_member = models.Member(
            id=ctx.author.id,
            username=ctx.author.name
        )
        bot.db.add(new_member)
        new_tracker= models.Tracker(
        track_url=url,
        title=title,
        available=True,  # Set initial values as necessary
        price=price,      # Set initial values as necessary
        member=member,  # Set the member relationship
        )
        bot.db.add(new_tracker)
        bot.db.commit
        await ctx.send(f"Success! I added it to the database. Will update you if the price changes or it goes out of stock :3")
    elif member and not existing_tracker:
            new_tracker = models.Tracker(
            track_url=url,
            title=title,
            available=True,  # Set initial values as necessary
            price=price,      # Set initial values as necessary
            member=member,  # Set the member relationship
            )
            bot.db.add(new_tracker)
            bot.db.commit
            await ctx.send(f"Success! I added it to the database. Will update you if the price changes or it goes out of stock :3")
    else:
        await ctx.send(f"I am already tracking this on the database. Stat queries are curretly a WIP!")



async def track_time(ctx, bot, data):
    new_bot_command = models.BotCommands(
         id=data.user_id,
         username=data.username,
         command=data.command,
         last_response=data.last_response,
         duration=data.duration
    )
    bot.db.add(new_bot_command)
    bot.db.commit()
    if "error" in data.last_response:
         await ctx.send(f"sorry you got an error :( feel free to suggest any input on how to make renachan.py better :) this command took f{data.duration} ms to complete that's so much for checking my bot out :)")
    else:
         await ctx.send(f"thanks so much for checking my discord bot out! this command took f{data.duration} ms to complete")
