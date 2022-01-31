VERSION = "2022-01-31"

import datetime
from http import server
import os
import random
import string
from termios import VERASE
import time

import functions.constants
from commands.openrace import openrace
from commands.joinrace import joinrace
from commands.done import done
from commands.getseed import getseed
from commands.gethistory import gethistory
from commands.getraces import getraces
from commands.closerace import closerace
from commands.killrace import killrace
from commands.testcommand import testcommand
from commands.raceinfo import raceinfo
from functions.string_functions import parse_command

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
    print(emessage)
    exit(1)


races = {}
load_dotenv()
client = discord.Client()

help ="""
FF6WC RaceRoom Bot - Test version %s

The bot currently supports the following commands:
    !help
        Prints this help text

    !openrace
        Opens a race. If no options are provided, the race will be synchronous (players must race at the same time) and a random name will be generated. A raceroom and spoiler room will be generated. The following options exist:
            -name <racename>: Open a race with the name <racename>. Must be between 1 and 29 characters
            -async: Opens an async race. Races are sync by default
            -hidden : Opens a sync race with a hidden seed which will only be rolled and DMed to the players right before start

    !closerace
        Removes a raceroom and its spoiler room after a brief delay

    !join <racename>
        Joins a race called <racename>, if it exists

    !done 11:22:33
        When used in a race room, marks a race as completed in the given time (in this case 11 hours, 22 minutes, and 33 seconds)

    !getseed
        Asks for a specfic seed for a given race, specified by the room the command is run in. This seed will be DMed to the user and a timer will start once it has been DMed. When the racer types !done, the total time between the DM and done command will be the runner's time

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

intents = discord.Intents.default()
intents.members = True

@client.event
async def on_ready():
    gmessage = f'FF6WC Racebot Version {VERSION}: We have logged in to as {client.user}'
    print(gmessage)

@client.event
async def on_message(message):
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

    if 'help' in commands_values.keys():
        await message.channel.send(help)
        if message.author.id in functions.constants.ADMINS:
            await message.channel.send(adminhelp)

    # Opens a race, creating a race channel and a spoiler channel for it
    if 'openrace' in commands_values.keys():
        new_race = await openrace(guild, message, commands_values)

        # If raceroom creation failed, don't add it to the list of rooms, but print a message
        if not new_race:
            emessage = f"Failed to create raceroom on {message.guild} in {message.channel}\n\t{message.author} - {message.content}"
            print(emessage)
            return
        races[new_race.channel.name] = new_race

    # This command adds a user to an existing race room
    if 'join' in commands_values.keys():
        await joinrace(guild, message, commands_values)

    # This command gets the seed specified for the given room
    if 'getseed' in commands_values.keys():
        await getseed(guild, message, commands_values, races)

    # This command gets information about the current race
    if message.content.startswith("!raceinfo"):
        await raceinfo(guild, message, commands_values, races)

    # This command adds a user to the spoiler channel when they're done
    if message.content.startswith("!done"):
        await done(guild, message, commands_values)

    # This message closes the race and spoiler rooms - definitely needs built out more
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

    # Admin only: Test stuff
    if message.content.startswith("!test"):
        await testcommand(message)

client.run(os.getenv('DISCORD_TOKEN'))

