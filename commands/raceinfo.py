import datetime
import discord
import random
import string

from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname


async def raceinfo(guild, message, args, races):
    """
    Gets information about the race in this room

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
    elif 'raceinfo' not in args.keys():
        emessage += f"args did not contain a 'raceinfo' key\n"
    if emessage != "":
        raise Exception(emessage)

    cat = get(guild.categories, name="racing")
    if message.channel.category == cat:
        race_channel = get(guild.channels, name=message.channel.name)
        if race_channel.name in races.keys():
            race = races[race_channel.name]
            msg = '`\n'
            msg += str(race)
            msg += '`\n'
            await message.channel.send(msg)

    else:
        await message.channel.send("This is not a race room!")