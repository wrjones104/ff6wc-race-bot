import datetime
import discord
import random
import string

from better_profanity import profanity
from discord.utils import get
from functions.add_racerooms import add_racerooms
from functions.string_functions import parse_roomname
from functions.generate_seed import generate_seed


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

    flags = "-cg -oa 2.2.2.2.7.7.4.10.10 -ob 30.8.8.1.1.11.8 -sc1 random -sc2 random -sal -eu -fst -brl -slr 1 5 -lmprp 75 125 -lel -srr 3 15 -rnl -rnc -sdr 1 1 -das -dda -dns -com 98989898989898989898989898 -rec1 28 -rec2 23 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 2 -hmced 2 -xgced 2 -ase 2 -msl 40 -sed -bbs -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 1 5 -ebr 68 -emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -smc 3 -ieor 33 -ieror 33 -csb 1 32 -mca -stra -saw -sisr 20 -sprp 75 125 -sdm 4 -npi -ccsr 20 -cms -cor -crr -crvr 255 255 -ari -anca -adeh -nfps -nu -fs -fe -fvd -fr -fj -fbs -fedc -as -ond -rr"
    seed = generate_seed(flags)
    url = seed['url']
    version = seed['version']
    hash = seed['hash']

    smessage = f"Here's your Worlds Collide version {version} seed:\n"
    smessage += f"URL: {url}\n"
    smessage += f"Hash: {hash}\n"
    smessage += "\n"
    author = message.author
    await author.send(smessage)