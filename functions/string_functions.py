import random
import string

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

    # Generate a random name of length k
    if name is None:
        return '-'.join(["ff6wc", ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))]).strip()

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
