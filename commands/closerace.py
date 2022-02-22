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
from functions.constants import TZ


async def closerace(guild, message, args, races, msg = None):
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

    msg : str (optional)
        A message to write out to the log

    Returns
    -------
    Nothing
    """

    if not message.channel.name in races.keys():
        await message.channel.send("This is not a race room!")
        return

    msg = "The follwing runners have not yet finished/forfeited:\n"
    stillrunning = False
    channel_name = message.channel.name
    for runner in races[channel_name].members:
        if not races[channel_name].members[runner].forfeit and not races[channel_name].members[runner].finish_date:
            stillrunning = True
            msg += f"\t{runner}\n"

    if stillrunning:
        await message.channel.send(msg)
        return

    race_channel = get(guild.channels, name=message.channel.name)
    spoiler_channel = get(guild.channels, name=''.join([str(race_channel), "-spoilers"]))


    msg = "This race is over! Here are the results:\n"
    await message.channel.send(msg)
    await message.channel.send(races[channel_name].getResults())

    await message.channel.send(f"This room and its spoiler room will be closed in {functions.constants.RACE_ROOM_CLOSE_TIME} seconds!")
    time.sleep(functions.constants.RACE_ROOM_CLOSE_TIME)

    if race_channel:
        await race_channel.delete()
    if spoiler_channel:
        await spoiler_channel.delete()

    msg = f"\nClosed by {message.author}"
    races[channel_name].comments += msg
    races[channel_name].close()
    del races[channel_name]
