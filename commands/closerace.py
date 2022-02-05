import datetime
import discord
import random
import string
import time
import datetime
from pytz import timezone

import functions.constants
from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname
from functions.lograce import lograce


async def closerace(guild, message, args, races):
    """
    User command to close out a race room and its spoiler room

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

    # TODO: Add in gating to prevent people from closing the room while folks are running - WhoDat42 - 2022-01-26
    cat = get(guild.categories, name="racing")
    if message.channel.category == cat:
        race_channel = get(guild.channels, name=message.channel.name)
        spoiler_channel = get(guild.channels, name=''.join([str(race_channel), "-spoilers"]))
        await message.channel.send(f"This room and its spoiler room will be closed in {functions.constants.RACE_ROOM_CLOSE_TIME} seconds!")
        time.sleep(functions.constants.RACE_ROOM_CLOSE_TIME)

        if race_channel:
            await race_channel.delete()
        if spoiler_channel:
            await spoiler_channel.delete()

        if race_channel.name in races.keys():
            tz = timezone('US/Eastern')
            races[race_channel.name].closed_date = datetime.datetime.now(tz)
            races[race_channel.name].comments = f"Closed by {message.author}"
            lograce(races[race_channel.name])

            del races[race_channel.name]
    else:
        await message.channel.send("This is not a race room!")