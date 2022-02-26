import datetime
import discord
import random
import string

from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname
from classes.RaceRunner import RaceRunner
from functions.constants import TZ, RACETYPE_ASYNC

async def joinrace(guild, message, args, races):
    """
    Joins a race in a given guild (server) with the name stored in args

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
    elif 'join' not in args.keys():
        emessage += f"args did not contain a 'join' key\n"
    elif 'room' not in args['join'].keys():
        emessage += f"args['join'] did not contain a 'room' key\n"
    if emessage != "":
        raise Exception(emessage)

    # The channel the message is in
    channel = message.channel

    if len(args['join']['room']) != 1:
        emessage = "Use !join <channel_name> to join a channel. Example: \n    !join ff6wc-abcdef-sync"
        await channel.send(emessage)
        return None

    c_name = args['join']['room'][0]
    join_channel = get(guild.channels, name=c_name)
    if not join_channel:
        emessage = f"The channel {c_name} does not exist"
        await channel.send(emessage)
        return


    race = races[join_channel.name]

    if message.author.name in race.members.keys():
        emessage = "You've already joined this race!"
        await channel.send(emessage)
        return

    rr = RaceRunner()
    rr.member = message.author
    rr.join_date = datetime.datetime.now(TZ)
    rr.race = race
    rr.guild = guild
    rr.channel = channel
    if race.type == RACETYPE_ASYNC:
        rr.ready = True

    race.addRacer(rr)


    join_msg = f"{message.author.name} has joined the race!"
    await join_channel.set_permissions(message.author, read_messages=True, send_messages=True)
    await join_channel.send(join_msg)
    await message.delete()

