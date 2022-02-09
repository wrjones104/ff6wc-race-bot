import datetime
import discord
import random
import string

from better_profanity import profanity
from discord.utils import get


from functions.isRace_room import isRace_room
from functions.constants import TZ, RACETYPE_ASYNC

async def startrace(guild, message, args, races):
    """
    starts a race in a given guild (server) with the name stored in args

    Parameters
    ----------
    guild : discord.guild.Guild
        The server we're on

    message : discord.message.Message
        A discord message containing our command

    args : dict
        A dictionary containing the command we've been given
        ex: {'join': {'room': ('myrace-sync',)}}

    Returns
    -------
    Nothing
    """
    emessage = ""
    if not isinstance(guild, discord.guild.Guild):
        emessage += f"guild is not a discord.guild.Guild - Found type {type(guild)}\n"
    if not isinstance(message, discord.message.Message):
        emessage += f"message is not a discord.message.Message - Found type {type(message)}\n"
    if not isinstance(args, dict):
        emessage += f"args is not a Python dict - Found type {type(args)}\n"
    if emessage != "":
        raise Exception(emessage)

    # The channel the message is in
    channel = message.channel
    if not isRace_room(channel, races):
        msg = "This is not a race room!"
        await channel.send(msg)
        return

    race = races[channel.name]
    # Make sure everyone is ready
    unready = []
    for member in race.members.keys():
        if not race.members[member].ready:
            unready.append(race.members[member].member.name)
    if len(unready) > 0:
        msg = "The following members are not ready:\n"
        for member in unready:
            msg += f"    {member}\n"
        await channel.send(msg)
        return

    race = races[channel.name]
    race.race_start_date = datetime.datetime.now(TZ)
    for member in race.members.keys():
        race.members[member].start_date = race.race_start_date

    msg = f"Race started at {race.race_start_date} ET. "
    if race.type == RACETYPE_ASYNC:
        msg += "Use the following command to enter your finish time: `!done hh:mm:ss.xxx`"
    else:
        msg += "To finish the race and record your time, type `!done` with no arguments."

    await channel.send(msg)