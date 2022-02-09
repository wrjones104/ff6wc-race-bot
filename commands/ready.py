import discord
from functions.isRace_room import isRace_room

async def ready(guild, message, args, races) -> dict:
    channel = message.channel

    if not isRace_room(channel, races):
        msg = "This is not a race room!"
        await channel.send(msg)
        return

    # Is the user in this race?
    race = races[channel.name]
    if message.author.name not in race.members.keys():
        msg = f"User {message.author.name} is not in this race"
        await message.channel.send(msg)
        return

    race.members[message.author.name].ready = True
    msg = f"User {message.author.name} is ready! "

    unready = []
    for member in race.members.keys():
        if not race.members[member].ready:
            unready.append(race.members[member].member.name)
    if len(unready) > 0:
        msg += f"{len(unready)} players are still unready."
    else:
        msg += "Everyone is ready! Use `!startrace` to start the race."

    await channel.send(msg)