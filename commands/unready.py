import discord
from functions.isRace_room import isRace_room

async def unready(guild, message, args, races) -> dict:
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

    race.members[message.author.name].ready = False
    msg = f"User {message.author.name} is not ready! "

    unready = 0
    for member in race.members.keys():
        if not race.members[member].ready:
            unready += 1

    msg += f"{unready} players are unready."

    await channel.send(msg)