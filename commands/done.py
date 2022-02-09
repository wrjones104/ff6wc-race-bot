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


async def done(guild, message, args, races) -> dict:
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

    if not race.members[message.author.name].start_date:
        msg = f"User {message.author.name} has not started this race"
        await message.channel.send(msg)
        return

    # There are many ways the user can screw this up, so we'll have to show this message a lot
    bad_time_message = "Use !done <time> to submit your time. Example: \n    !done 00:34:18.76\n"

    ## First, if there's some sort of weird error on our part or they didn't submit a string. If this is not
    ## an async, we don't need to do any of this since we just care about when they typed !done
    dt = None
    done_str = None
    if race.type == RACETYPE_ASYNC:
        if len(args['done']['time']) != 1 or not isinstance(args['done']['time'][0], str):
            await channel.send(bad_time_message)
            return None

        done_time = args['done']['time'][0]

        # This function returns a datetime.timedelta and passes it to our string parser
        try:
            dt = parse_done_time(done_time)
        except Exception as e:
            await channel.send(bad_time_message)
            return None


    race.members[message.author.name].forfeit = False
    race.members[message.author.name].finish_date = datetime.datetime.now(TZ)

    # If this is a hidden seed or sync, the racers don't report their own time
    if race.type == RACETYPE_ASYNC:
        race.members[message.author.name].start_date = race.members[message.author.name].finish_date - dt

    done_str = timedelta_to_str(race.members[message.author.name].time_taken)

    # Finally we should have a reasonable time
    done_msg = f"{message.author.name} has finished the race with a time of {done_str}!"
    spoiler_channel = get(guild.channels, name=message.channel.name + "-spoilers")
    await spoiler_channel.set_permissions(message.author, read_messages=True, send_messages=True)
    spoil_msg = await spoiler_channel.send(done_msg)
    await spoil_msg.pin()

    # Check to see if everyone is done
    for member in race.members.keys():
        if not race.members[member].finish_date:
            return

    # Everyone is done, print the results and close the race
    msg = "This race is over! Here are the results:\n"
    await channel.send(msg)
    await channel.send(race.getResults())
    await closerace(guild, message, args, races, "Race ended normally")

