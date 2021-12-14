import datetime
import os
import random
import string
import time
from commands.startrace import startrace
from commands.joinrace import joinrace
from commands.done import done
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
except ModuleNotFoundError:
    missing_imports.append("discord")

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    missing_imports.append("dotenv")

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
JONES = 197757429948219392
WHODAT = 763412923409760296

help ="""
FF6WC Race Bot - Test version 2021-12-14-0230

The bot currently supports the following commands:
    !help
        Prints this help text

    !startrace
        Starts a race. If no options are provided, the race will be synchronous (players must race at the same time) and a random name will be generated. A raceroom and spoiler room will be generated. The following options exist:
            -name <racename>: Start a race with the name <racename>. Must be between 1 and 29 characters
            -async: Starts an async race. Races are sync by default

    !join <racename>
        Joins a race called <racename>, if it exists

    !done 11:22:33
        When used in a race room, marks a race as completed in the given time (in this case 11 hours, 22 minutes, and 33 seconds)

    !getrooms
        A command for administrators which shows the current races

"""

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # "guild" is the server name. The following variable is just storing the name of the server that the message
    # originated from
    guild = message.author.guild

    # This command just keeps the bot from issuing itself commands
    if message.author == client.user:
        return

    # A dictionary with commands as keys and arguments to those commands as values. For example:
    #   !startrace -name TestRoom1 -argument2 Something
    # gives
    #   {'startrace': {'name': ('TestRoom1',), 'argument2': ('Something',)}}

    if message.content.startswith("!"):
        commands_values = parse_command(message.content)
        ## Uncomment below for debugging
        #print(commands_values)

    if 'help' in commands_values.keys():
        await message.channel.send(help)

    # Test message just to see bot response
    if message.content.startswith("$hello"):
        await message.channel.send("Hello to you!")

    # Starts a race, creating a race channel and a spoiler channel for it
    if 'startrace' in commands_values.keys():
        name_type = await startrace(guild, message, commands_values)
        for roomname in name_type.keys():
            races[roomname] = name_type[roomname]

    # This command adds a user to an existing race room
    if 'join' in commands_values.keys():
        await joinrace(guild, message, commands_values)

    # This command adds a user to the spoiler channel when they're done
    if message.content.startswith("!done"):
        await done(guild, message, commands_values)


    # This message closes the race and spoiler rooms - definitely needs built out more
    if message.content.startswith("!finishasync"):
        cat = get(guild.categories, name="racing")
        if message.channel.category == cat:
            race_channel = get(guild.channels, name=message.channel.name)
            spoiler_channel = get(guild.channels, name=''.join([str(race_channel), "-spoilers"]))
            await message.channel.send("This room and its spoiler room will be closed in 1 minute!")
            time.sleep(60)

            await race_channel.delete()
            await spoiler_channel.delete()
            del races[str(race_channel)]
        else:
            await message.channel.send("This is not a race room!")

    if message.content.startswith("!getrooms"):
        if message.author.id not in (JONES, WHODAT):
            await message.channel.send("Wait a second... you're not a Presenter fan!")
        else:
            rmessage = ""
            if len(races.keys()) == 0:
                rmessage = "There are no active races"
            else:
                rmessage = f"Currently there are {len(races.keys())} active races:\n"
                for race in races:
                    rmessage += f"    {race} - {races[race]}\n"
            await message.channel.send(rmessage)
            races_file_path = "db/races.txt"
            try:
                with open(races_file_path, 'r') as f:
                    m_msg = f.read()
                    f.close()
                    await message.channel.send(m_msg)
            except Exception as e:
                print ("Unable to read from %s" % races_file_path)
client.run(os.getenv('DISCORD_TOKEN'))
