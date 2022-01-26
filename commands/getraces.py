import functions.constants

async def getraces(message, races):
    """
    Gets a list of active races. Must be an admin

    Parameters
    ----------
    message : discord.message.Message
        A discord message containing our command

    races : dict
        A dictionary containing racerooms

    Returns
    -------
    Nothing
    """

    if message.content.startswith("!getraces"):
        if message.author.id not in functions.constants.ADMINS:
            return
        rmessage = ""
        if len(races.keys()) == 0:
            rmessage = "There are no active races"
        else:
            rmessage = f"Currently there are {len(races.keys())} active races:\n"
            for race in races:
                rmessage += f"    {race} - {races[race]}\n"
        await message.channel.send(rmessage)