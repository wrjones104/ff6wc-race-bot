import discord
import os
import time
import random
import string
from discord.utils import get
import datetime

from dotenv import load_dotenv


load_dotenv()

client = discord.Client()


def add_racerooms(user, room_id, room_type, spoiler_room, ts):
    f = open("db/races.txt", "a")
    writemsg = str([user, room_id, room_type, spoiler_room, ts])+"\n"
    f.write(writemsg)
    f.close()


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

    # Make a list of all text following the first string in the command
    if message.content.startswith("!"):
        args = message.content.split("-")[1:]
        jargs = message.content.split(' ')[1:]

    # Test message just to see bot response
    if message.content.startswith("$hello"):
        await message.channel.send("Hello to you!")

    # This command is all about channel creation
    if message.content.startswith("!startrace"):

        # This next part just pulls the category name for channel creation.
        cat = get(guild.categories, name="racing")

        # This stores the name of the channel, which can be different based on any arguments given by the user
        if 'name' in ''.join(args):
            c_name = str.lower([s for s in args if "name" in s][0].translate(str.maketrans('', '', string.punctuation))
                               .replace('name ', '').rstrip()).replace(" ", "-")
        else:
            c_name = '-'.join(["ff6wc", ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))])

        if 'async' in ''.join(args):
            c_name += '-async'
            room_type = "Async"
        else:
            room_type = "Sync"

        # This makes the channel private
        race_room_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            message.author: discord.PermissionOverwrite(read_messages=True)
        }

        spoiler_room_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        # This creates the channel, pulling in the channel name (c_name), category (cat) and overwrites (overwrites)
        race_channel = await guild.create_text_channel(c_name, category=cat, overwrites=race_room_overwrites)
        spoiler_channel = await guild.create_text_channel('-'.join([c_name, "spoilers"]), category=cat,
                                                          overwrites=spoiler_room_overwrites)

        add_racerooms(str(message.author.id), str(race_channel.id), room_type, str(spoiler_channel.id),
                      str(datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")))


        # This stores the new channel for the bot to message in after creation
        # new_channel = get(guild.channels, name=c_name)

        # This sends a message in the new channel after a 2-second delay
        # I'd rather change this to a loop to check if the channel exists - I'm just using the timer now to keep from
        # the message firing before the channel is created
        r_create_msg = ''.join(["Welcome to your shiny new race room, ", str(message.author.name), "!"])
        await race_channel.send(r_create_msg)

        # This sends the confirmation and join message to the requestor's channel
        create_msg = ' '.join(["Your race room has been created. Type `!join", c_name + "`", "to join the channel!"])
        await message.channel.send(create_msg)

    # This command adds a user to an existing race room
    if message.content.startswith("!join"):
        join_channel = get(guild.channels, name=jargs[0])
        join_msg = ' '.join([message.author.name, "has joined the race!"])
        await join_channel.set_permissions(message.author, read_messages=True, send_messages=True)
        await join_channel.send(join_msg)
        # await message.delete()

    # This command adds a user to the spoiler channel when they're done
    if message.content.startswith("!done"):
        done_time = jargs[0]
        done_msg = ''.join([message.author.name, " has finished the race with a time of ", done_time, "!"])
        this_channel = ''.join([message.channel.name, "-spoilers"])
        spoiler_channel = get(guild.channels, name=this_channel)
        await spoiler_channel.set_permissions(message.author, read_messages=True, send_messages=True)
        spoil_msg = await spoiler_channel.send(done_msg)
        await spoil_msg.pin()

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
        else:
            await message.channel.send("This is not a race room!")

    if message.content.startswith("!getrooms"):
        if message.author.id == 197757429948219392:
            with open("db/races.txt") as f:
                m_msg = f.read()
                f.close()
                await message.channel.send(m_msg)
        else:
            await message.channel.send("Wait a second... you're not Jones!")


client.run(os.getenv('DISCORD_TOKEN'))
