import datetime
import discord
import random
import string
import time
import datetime

import functions.constants
from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname
from functions.isRace_room import isRace_room


async def entrants(guild, message, args, races):
    """
    Get list of entrants

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
    channel = message.channel
    if not isRace_room(channel, races):
        msg = "This is not a race room!"
        await channel.send(msg)
        return

    race = races[channel.name]

    msg = '`'
    if len(race.members) == 0:
        msg = "This race doesn't have any entrants yet!"
    else:
        for member in race.members.keys():
            status = "Not Ready"
            if race.members[member].ready:
                status = "Ready"
            if race.members[member].start_date:
                status = "Running"
            if race.members[member].finish_date:
                status = "Finished"
            if race.members[member].forfeit:
                status = "FF"

            msg += race.members[member].member.name + '--'+ status + '\n'
        msg += '`\n'
    await message.channel.send(msg)