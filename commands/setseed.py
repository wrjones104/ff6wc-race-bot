import datetime
import discord
import random
import string

from better_profanity import profanity
from discord.utils import get

from classes.Log import Log
import functions.constants
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname
from functions.generate_seed import generate_seed
from functions.isRace_room import isRace_room


async def setseed(guild, message, args, races):
    """
    Sets the guarded async seed for this channel
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
    logger = Log()

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
    if not isRace_room(channel, races):
        msg = "This is not a race room!"
        await channel.send(msg)
        return
    channel_name = str(channel)

    race = races[channel_name]

    isFlagset = False
    # Use this to parse a flagset
    if ('' in args['setseed'] and "https" not in args['setseed']['']) or '' not in args['setseed']:
        flagstr = ""
        for key in args['setseed'].keys():
            flagstr += f"-{key} " + (' ').join(args['setseed'][key]) + " "
        while "  " in flagstr:
            flagstr = flagstr.replace("  ", " ")

        try:
            seed = generate_seed(flagstr)
            assert seed["url"]
            race.flags = flagstr
            race.url = seed["url"]
            race.version = seed["version"]
            race.hash = seed["hash"]

        except Exception as e:
            emessage = f"Unable to generate seed from the given flags:\n{flagstr}\n"
            await channel.send(emessage)
            logger.show(emessage, functions.constants.LOG_CRITICAL)
            logger.show(str(e), functions.constants.LOG_CRITICAL)
            return

        isFlagset = True

    if not isFlagset:
        try:
            assert '' in args['setseed'].keys()
        except:
            log_msg = f"\n{guild} -- There was an error in the setseed function:\n{args}\n"
            emessage += "There was an error in the setseed function. Contact WhoDat42 or wrjones18"
            await channel.send(emessage)
            logger.show(emessage, functions.constants.LOG_CRITICAL)
            return None

    # Check to see if this is a racing channel
    if channel_name not in races.keys():
        emessage = f"{channel_name} is not a race channel. Not sending seed."
        await channel.send(emessage)
        return None

    #race = races[channel_name]

    # Make sure the user here is an admin
    if not message.author.id in race.admins:
        emessage = f"{message.author} is not an admin of the race in channel {channel_name}"
        await channel.send(emessage)
        return None

    if not isFlagset:
        try:
            race.url = args['setseed'][''][0]
            msg = "Seed URL set"
            await channel.send(msg)
        except Exception as e:
            msg = "Set a seed (not flags) using the following syntax:\n"
            msg += "!setseed <URL> or !setseed <flagset>\n"
            msg += "    *ex: !setseed https://ff6wc.com/seed/E6n93pxzhYEs*\n\n"
            await channel.send(msg)
            return

    if race.isHidden:
        await message.delete()
        msg = f"The seed has been set!\n"
        await channel.send(msg)
    else:
        msg = f"The seed has been set!\n"
        if not isFlagset:
            msg += f"Here is the seed link for this race -- {race.url}"
        else:
            msg += f"Here are the flags:\n{race.flags}\n"
        seedmsg = await channel.send(msg)
        await seedmsg.pin()




