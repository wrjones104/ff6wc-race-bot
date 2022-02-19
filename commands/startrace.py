import datetime
import discord
import random
import string

from better_profanity import profanity
from discord.utils import get
import traceback

from commands.getseed import getseed_hidden
from functions.isRace_room import isRace_room
from functions.constants import TZ, RACETYPE_ASYNC, LOG_TRIVIAL, RACETYPE_SYNC
from classes.Log import Log

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

    races : dict
        A dictionary containing racerooms

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

    if not race.url:
        emessage = "This race doesn't have a seed yet, so it can't be started."
        await channel.send(emessage)
        return

    if len(race.members.keys()) == 0 and race.type == RACETYPE_SYNC:
        emessage = "There are no racers yet!"
        await channel.send(emessage)
        return

    # Make sure everyone is ready if it's a sync
    if race.type == RACETYPE_SYNC:
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

    if race.race_start_date:
        msg = "This race has already been started. Get going!"
        await channel.send(msg)
        return

    race = races[channel.name]
    race.race_start_date = datetime.datetime.now(TZ)

    # It's a hidden sync race, so send everyone the seed at once
    if race.isHidden and race.type == RACETYPE_SYNC:
        for member in race.members.keys():
            user = race.members[member].member
            race.url = await getseed_hidden(user, race)

    # It's a sync race, so everyone starts at the same time
    if race.type == RACETYPE_SYNC:
        for member in race.members.keys():
            race.members[member].start_date = race.race_start_date

    race.log(LOG_TRIVIAL)

    msg = f"Race started at {race.race_start_date} ET. "

    if race.isHidden and race.type == RACETYPE_ASYNC:
        msg += "\nThe race has started. You may request the seed with `!getseed`\n"
        msg += "Your timer will start once you have been DMed.\n"

    if race.type == RACETYPE_ASYNC and not race.isHidden:
        msg += "Use the following command to enter your finish time: `!done hh:mm:ss.xxx`"
    else:
        msg += "To finish the race and record your time, type `!done` with no arguments."

    await channel.send(msg)
    race.log(LOG_TRIVIAL)
    logger = Log()
    pmsg = f"{message.guild} -- Race {channel.name} has started!"
    logger.show(pmsg)