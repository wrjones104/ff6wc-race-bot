import random
import string
import datetime

from better_profanity import profanity
from functions.constants import RANDOM_ROOM_NAME_LENGTH

dashes = ('-', '\u002d', '\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2e3a', '\u2e3b', '\ufe58', '\ufe63', '\uff0d')

def parse_command(in_string: str) -> str:
    """
    Parses commands for our bot. Ensures that they are formatted correctly, not that the commands work.

    Parameters
    ----------
    in_string : str
        The input command string

    Returns
    -------
    dict
        A dictionary mapping commands to their values. Values themselves will be dictionaries if they start with a dash
    """

    # If the input isn't a string, raise an exception
    if not isinstance(in_string, str):
        message = "Input must be a string. Found type %s." % type(in_string)
        raise Exception(message)

    # If the input doesn't have exactly one !, raise an exception
    in_string = in_string.strip()
    if not in_string.startswith("!"):
        message = "There has been a programming error. The bot is attempting to parse a command which does not "
        message += "start with '!'. I blame Jones."
        raise Exception(message)
    if in_string.count("!") > 1:
        message = "Error! Cannot have more than one command per line. Found the following commands:\n"
        for i in in_string.split("!")[1:]:
            message += "    " + i.split(" ")[0] + "\n"
        raise Exception(message)

    # Turn all possible unicode dashes in to a regular dash and turn all multiple spaces into one space
    for dash in dashes:
        in_string = in_string.replace(dash, '-')
    while '  ' in in_string:
        in_string = in_string.replace('  ', ' ')

    # Check to make sure the command isn't empty. If it is, raise an exception
    commands_values = {}
    command = in_string.split(" ")[0][1:]
    if command == '':
        message = "Received empty command."
        raise Exception(message)


    # Check for arguments like -name. We check for ' -' because room names will have dashes in them.
    # We need to avoid confusing those for arguments
    if ' -' in in_string:
        args = in_string.split(" -")[1:]
        commands_values[command] = {}
        for s in in_string.split(" -")[1:]:
            arguments = s.split(' ')
            arg = arguments[0].strip()
            values = tuple([value.strip() for value in arguments[1:] if value != ''])
            commands_values[command][arg] = values
    else:
        value = tuple(in_string.split(' ')[1:])
        commands_values[command] = {}
        key = ''
        if command == 'join':
            key = "room"
        if command == "done":
            key = "time"
        commands_values[command][key] = value

    return commands_values


def parse_roomname(name=None) -> str:
    """
    Parses the arguments for a named room, returning a name conforming to our rules. Use of this function
    assumes that the command has been run through our ``parse_command`` function. If no name is supplied, one
    will be created.

    Paramters
    ---------
    name : str (optiona)
        The name of the room

    Returns
    -------
    str
        The name of the room to be created
    """

    # Generate a random name of length functions.constants.RANDOM_ROOM_NAME_LENGTH. Check them for profanity and reroll if it exists
    if name is None:
        counter = 0
        room_name = '-'.join(["ff6wc", ''.join(random.choices(string.ascii_lowercase + string.digits, k=RANDOM_ROOM_NAME_LENGTH))]).strip()
        while profanity.contains_profanity(room_name):
            room_name = '-'.join(["ff6wc", ''.join(random.choices(string.ascii_lowercase + string.digits, k=RANDOM_ROOM_NAME_LENGTH))]).strip()
            counter += 1
            if counter > 100:
                emessage = "Attempted to create 100 random room names and they all contain profanity. Ending attempts."
                raise Exception(emessage)
        return room_name

    # Try to use the name the user provided
    if not isinstance(name, str):
        message = "Input name must be a string. Found type %s" % type(name)
        raise Exception(message)
    if not 0 < len(name) < 30:
        message = "Room name must be between 1 and 29 characters, inclusive. Found length of %s" % len(name)
        raise Exception(message)
    name = name.strip().lower()
    for c in "!\"#$%&'()*+,./:;<=>?@[\]^_`{|}~ ":
        name = name.replace(c, '-')
    while '--' in name:
        name = name.replace('--', '-')

    return name

def parse_done_time(input:str) -> datetime.timedelta:
    """
    Parses the input string representing the done time for a race. We expect something like this:
        01:23:45.6789
    which represents 1h 23m 45.6789s

    Unfortunately we may get any sort of crazy input.
    """
    if not isinstance(input, str):
        emessage = f"Expected time input of type str. Found type {type(input)}"
        raise Exception(emessage)

    if not 0 < input.count(":") < 3:
        emessage = f"Expected time in the format of hh:mm:ss.xxxx or mm:ss.xxxx. Found {input}"
        raise Exception(emessage)

    ##Split the time by colons
    hours = 0
    minutes = 0
    seconds = 0
    time_split = input.split(':')
    seconds = time_split[-1]
    minutes = time_split[-2]
    if len(time_split) == 3:
        hours = time_split[0]

    try:
        hours = int(hours)
        assert 24 > hours >= 0

        minutes = int(minutes)
        assert 60 > minutes >= 0

        seconds = float(seconds)
        assert 60 > seconds >= 0

    except Exception as e:
        emessage = f"Time can't be 24+ hours or have more than 59 minutes or seconds. Found {input}"
        raise Exception(emessage)
    donetime = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return donetime

def timedelta_to_str(input:datetime.timedelta) -> str:
    """Converts a datetime.timedelta value to a string formatted as hh:mm:ss.xx"""
    if not isinstance(input, datetime.timedelta):
        emessage = f"input must be datetime.timedelta. Found type {type(input)}"
        raise Exception(emessage)
    hours, remainder = divmod(input.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds = int(seconds)
    fraction = int(input.microseconds / 10000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{fraction}"
