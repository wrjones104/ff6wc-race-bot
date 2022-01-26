import datetime
import discord
import random
import string

from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname


async def getseed(guild, message, args, races):
    """
    Gets the guarded async seed for this channel and DMs it to the user

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

    # The channel the message is in. This is a discord channel object
    channel = message.channel
    channel_name = str(channel)

    try:
        assert '' in args['getseed'].keys()
    except:
        emessage += "There was an error in the getseed function. Contact WhoDat42 or wrjones18"
        await channel.send(emessage)
        return None

    # Make sure the user isn't trying to pass anything to the command
    if len(args.keys()) != 1 or 'getseed' not in args.keys() or len(args['getseed']['']) != 0:
        emessage += "Do not pass any commands to the getseed command"
        await channel.send(emessage)
        return None

    # Check to see if this is a racing channel
    if channel_name not in races.keys():
        emessage = f"{channel_name} is not a race channel. Not sending seed."
        await channel.send(emessage)
        return None

    smessage = f"Sending Seed!"
    author = message.author
    await author.send(smessage)