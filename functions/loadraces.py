
import os
import sys

def loadraces(path: str, client:discord.client.Client) -> dict:
    """
    Read in the currently active races from the filesystem given by path

    Parameters
    ----------
    path : str
        The root directory of where we store the race information

    client : discord.client.Client
        The bot client

    Returns
    -------
    dict
        A dictionary of the races. Each key is a server id with a value of another dictionary whose keys are raceroom names
        Those values are the races themselves
    """
    if not isinstance(path, str):
        emessage = f"input path must be a str. Found type {type(path)}"
        raise Exception(emessage)

    if not isinstance(client, discord.client.Client):
        emessage = f"client must be a discord.client.Client. Found type {type(path)}"
        raise Exception(emessage)

    servers = []
    directories = [w[0] for w in os.walk(input)]
    for directory in directories:
        directory = directory.strip().replace('/', '').replace('\\', '')
        if client.get_guild(directory):
            servers.append(directory)

