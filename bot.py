VERSION = "2022-02-21"

import datetime
from http import server
import os
import random
import string
from termios import VERASE
import time

import functions.constants
from functions.constants import LOG_CRITICAL, LOG_REGULAR
from commands.openrace import openrace
from commands.joinrace import joinrace
from commands.done import done
from commands.entrants import entrants
from commands.forfeit import forfeit
from commands.getseed import getseed
from commands.gethistory import gethistory
from commands.getraces import getraces
from commands.closerace import closerace
from commands.killrace import killrace
from commands.quit import quit
from commands.raceinfo import raceinfo
from commands.setseed import setseed
from commands.startrace import startrace
from commands.testcommand import testcommand
from commands.ready import ready
from commands.unready import unready

from functions.create_race_channels import create_race_channels
from functions.string_functions import parse_command
from functions.loadraces import loadraces
from classes.Log import Log

logger = Log()

# Check for missing imports
missing_imports = []
try:
    import better_profanity
except ModuleNotFoundError:
    missing_imports.append("better_profanity")

try:
    import discord
    from discord.utils import get
    from discord.ext import commands
except ModuleNotFoundError:
    missing_imports.append("discord")

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    missing_imports.append("python-dotenv")

if len(missing_imports) != 0:
    emessage = "Please install the following Python 3 packages before running the bot:\n"
    for mi in missing_imports:
        emessage += "    %s\n" % mi
    emessage += "\n"
    logger.show(emessage, LOG_CRITICAL)
    exit(1)


races = {}
load_dotenv()
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents = intents)

help ="""
FF6WC RaceRoom Bot - Test version %s

The bot currently supports the following commands:
    !help
        Prints this help text

    !openrace
        Opens a race. If no options are provided, the race will be synchronous (players must race at the same time) and a random name will be generated. A raceroom and spoiler room will be generated. The following options exist:
            -name <racename>: Open a race with the name <racename>. Must be between 1 and 29 characters
            -async: Opens an async race. Races are sync by default
            -hidden : Opens a race with a hidden seed which will only be rolled and DMed to the players right before start

            You may combine -async and -hidden to make a hidden async race

    !closerace
        Removes a raceroom and its spoiler room after a brief delay

    !join <racename>
        Joins a race called <racename>, if it exists

    !startrace
        Starts a race

    !ready / !unready
        Ready or unready yourself for a race

    !quit
        Quits a race

    !forfeit / !ff
        Forfeits from a race

    !entrants
        Lists the entrants of a race

    !raceinfo
        Lists information about a race

    !done / !done 11:22:33
        When used in a race room, marks a race as completed in the given time (in this case 11 hours, 22 minutes, and 33 seconds)
        For hidden seeds or asyncs, just use !done

    !getseed
        Asks for a specfic seed for a given race, specified by the room the command is run in. This seed will be DMed to the user and a timer will start once it has been DMed. When the racer types !done, the total time between the DM and done command will be the runner's time

    !setseed
        Sets the seed URL for a race. Can only be called by channel or race admins

""" % (VERSION)

adminhelp = """\n
Admin-only commands:
    !getraces
        A command for administrators which shows the current races

    !gethistory
        Get the history of races, stored in db/races.txt

    !killrace
        Immediately closes a race room and its spoiler room. This does not check to see if all racers are finished

"""

races = {}

@client.event
async def on_ready():
    global races

    gmessage = f'FF6WC Racebot Version {VERSION}: We have logged in {client.user}'
    logger.show(gmessage, LOG_CRITICAL)

    # The bot has just restarted, so read in the races we know about
    races = loadraces(functions.constants.RACE_PATH, client)

    gmessage = f"Found {len(races.keys())} open races\n"
    for r in races.keys():
        gmessage += f"    {races[r].guild} - {r}\n"
    logger.show(gmessage, LOG_CRITICAL)
    for key in races.keys():
        guild = races[key].guild
        creator = races[key].creator
        name = races[key].channel_name
        if not name:
            name = key
        await create_race_channels(guild, creator, name, logger)
        if not races[key].channel:
            races[key].channel = discord.utils.get(client.get_all_channels(), name=races[key].channel_name)

        for i in races[key].members.keys():
            if not races[key].members[i].channel:
                races[key].members[i].channel = races[key].channel

@client.event
async def on_message(message):
    global races
    # guild is the server name. The following variable is just storing the name of the server that the message
    # originated from. Check the type of channel to prevent throwing an error when the user is DMed
    if isinstance(message.channel, discord.channel.TextChannel):
        guild = message.channel.guild

    # This command just keeps the bot from issuing itself commands
    if message.author == client.user:
        return

    # A dictionary with commands as keys and arguments to those commands as values. For example:
    #   !openrace -name TestRoom1 -argument2 Something
    # gives
    #   {'openrace': {'name': ('TestRoom1',), 'argument2': ('Something',)}}

    if not message.content.startswith("!"):
        return

    # Beyond this point, all messages start with !
    commands_values = parse_command(message.content)

    if message.content.startswith("!help"):
        await message.channel.send(help)
        if message.author.id in functions.constants.ADMINS:
            await message.channel.send(adminhelp)

    # Opens a race, creating a race channel and a spoiler channel for it
    if message.content.startswith("!openrace"):
        new_race = await openrace(guild, message, commands_values)

        # If raceroom creation failed, don't add it to the list of rooms, but print a message
        if not new_race:
            emessage = f"{message.guild} -- Failed to create raceroom in {message.channel}\n\t{message.author} - {message.content}"
            logger.show(emessage, LOG_CRITICAL)
            return
        races[new_race.channel.name] = new_race

    # This command adds a user to an existing race room
    if message.content.startswith("!join"):
        await joinrace(guild, message, commands_values, races)

    # This command gets the seed specified for the given room
    if message.content.startswith("!getseed"):
        await getseed(guild, message, commands_values, races)

    # This command gets information about the current race
    if message.content.startswith("!raceinfo"):
        await raceinfo(guild, message, commands_values, races)

    # This command gets information about the entrants for this race
    if message.content.startswith("!entrants"):
        await entrants(guild, message, commands_values, races)

    # This command adds a user to the spoiler channel when they're done
    if message.content.startswith("!done"):
        await done(guild, message, commands_values, races)

    # This command starts a race
    if message.content.startswith("!startrace"):
        await startrace(guild, message, commands_values, races)

    # These commands ready or unready a player
    if message.content.startswith("!ready"):
        await ready(guild, message, commands_values, races)

    if message.content.startswith("!unready"):
        await unready(guild, message, commands_values, races)

    # Quit the race
    if message.content.startswith("!quit"):
        await quit(guild, message, commands_values, races)

    # Forfeit
    if message.content.startswith("!ff") or message.content.startswith("!forfeit"):
        await forfeit(guild, message, commands_values, races)

    # Close the race
    if message.content.startswith("!closerace"):
        await closerace(guild, message, commands_values, races)

    # Admin only: This message instantly closes the race and spoiler rooms
    if message.content.startswith("!killrace"):
        await killrace(guild, message, commands_values, races)

    # Admin only: Get current race rooms
    if message.content.startswith("!getraces"):
        await getraces(message, races)

    # Admin only: Get historical races
    if message.content.startswith("!gethistory"):
        await gethistory(message)

    # Admin only: Set room seed
    if message.content.startswith("!setseed"):
        await setseed(guild, message, commands_values, races)

    # Admin only: Test stuff
    if message.content.startswith("!test"):
        await testcommand(message)



client.run(os.getenv('DISCORD_TOKEN'))

