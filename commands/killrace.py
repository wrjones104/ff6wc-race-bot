import datetime
import discord
import random
import string
import time

from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname
import functions.constants


async def killrace(guild, message, args, races):
    """
    Admin only - Immediately removes a race room and its spoiler room

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
    if message.content.startswith("!getraces"):
        if message.author.id not in functions.constants.ADMINS:
            return

    cat = get(guild.categories, name="racing")
    if message.channel.category == cat:
        race_channel = get(guild.channels, name=message.channel.name)
        spoiler_channel = get(guild.channels, name=''.join([str(race_channel), "-spoilers"]))
        await message.channel.send("This room and its spoiler room will be closed in 1 second!")
        time.sleep(1)

        await race_channel.delete()
        await spoiler_channel.delete()
        del races[str(race_channel)]
    else:
        await message.channel.send("This is not a race room!")