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
from functions.lograce import lograce


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

    # TODO: Add in gating to prevent people from closing the room while folks are running - WhoDat42 - 2022-01-26
    cat = get(guild.categories, name="racing")
    race_channel = get(guild.channels, name=message.channel.name)
    if message.channel.category != cat or race_channel.name not in races.keys():
        await message.channel.send("This is not a race room!")
        return
    race = races[race_channel.name]

    msg = '`'
    if len(race.members) == 0:
        msg = "This race doesn't have any entrants yet!"
    else:
        for runner in race.members:
            msg += runner.member.name + '\n'
        msg += '`\n'
    await message.channel.send(msg)