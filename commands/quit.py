import datetime
from commands.closerace import closerace
import discord
import random
import string
from functions.constants import TZ, RACETYPE_ASYNC

from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname, parse_done_time, timedelta_to_str
from functions.isRace_room import isRace_room


async def quit(guild, message, args, races) -> dict:
    """
    Quits the race

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
    elif 'quit' not in args.keys():
        emessage += f"args did not contain a 'quit' key\n"

    if emessage != "":
        raise Exception(emessage)

    # The channel the message is in
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
    racer = race.members[message.author.name]
    race.removeRacer(racer)

    msg = f"User {message.author.name} has been removed from the race"
    await message.channel.send(msg)
