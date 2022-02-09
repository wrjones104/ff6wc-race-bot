import discord

def isRace_room(channel, races) -> bool:
    if not isinstance(channel, discord.channel.TextChannel):
        emessage = f"channel should be a discord.channel.TextChannel. Found type {type(channel)}"
        raise Exception(emessage)
    if not isinstance(races, dict):
        emessage = f"races should be a dictionary of Race objects. Found type {type(races)}"

    return channel.name in races.keys()