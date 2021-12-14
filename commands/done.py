import datetime
import discord
import random
import string

from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname


async def done(guild, message, args) -> dict:
    """
    Sets the user's finish time

    Parameters
    ----------
    guild : discord.guild.Guild
        The server we're on

    message : discord.message.Message
        A discord message containing our command

    args : dict
        A dictionary containing the command we've been given
        ex: {'done': {'time': ('1:23:04',)}}

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
    elif 'done' not in args.keys():
        emessage += f"args did not contain a 'done' key\n"
    elif 'time' not in args['done'].keys():
        emessage += f"args['done'] did not contain a 'time' key\n"

    if emessage != "":
        raise Exception(emessage)

    # The channel the message is in
    channel = message.channel

    # Are we in a race room? There's probably need for a more robust test for this
    if "sync" not in message.channel.name or "spoiler" in message.channel.name:
        emessage = "This isn't a race room!"
        await channel.send(emessage)
        return None

    # There are many ways the user can screw this up, so we'll have to show this message a lot
    bad_time_message = "Use !done <time> to submit your time. Example: \n    !done 00:34:18\n"

    ## First, if there's some sort of weird error on our part or they didn't submit a string
    if len(args['done']['time']) != 1 or not isinstance(args['done']['time'][0], str):
        await channel.send(bad_time_message)
        return None

    done_time = args['done']['time'][0]

    ## Second, if they put in some weird number of colons
    if not 0 < done_time.count(":") < 3:
        await channel.send(bad_time_message)
        return None

    ## Third, split the time by colons, cutting off the decimal points and checking for sanity
    hours = 0
    minutes = 0
    seconds = 0
    time_split = done_time.split(':')
    seconds = time_split[-1].split('.')[0]
    minutes = time_split[-2]
    if len(time_split) == 3:
        hours = time_split[0]

    try:
        hours = int(hours)
        assert 10 > hours >= 0

        minutes = int(minutes)
        assert 60 > minutes >= 0

        seconds = int(seconds)
        assert 60 > seconds >= 0
    except Exception as e:
        await channel.send(bad_time_message)
        return None

    # Finally we should have a reasonable time
    done_msg = f"{message.author.name} has finished the race with a time of {hours}:{minutes}:{seconds}!"
    spoiler_channel = get(guild.channels, name=message.channel.name + "-spoilers")
    await spoiler_channel.set_permissions(message.author, read_messages=True, send_messages=True)
    spoil_msg = await spoiler_channel.send(done_msg)
    await spoil_msg.pin()

    #this_channel = ''.join([message.channel.name, "-spoilers"])