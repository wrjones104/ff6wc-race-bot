import discord
import os


from dotenv import load_dotenv


load_dotenv()

client = discord.Client()


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
    args = message.content.split(" ")[1:]

    # Test message just to see bot response
    if message.content.startswith("$hello"):
        await message.channel.send("Hello to you!")

    # This command is all about channel creation
    if message.content.startswith("$channel"):

        # This next part just pulls the category name for channel creation. In the real server, the name would be
        # "racing"
        cat = discord.utils.get(guild.categories, name="bot-channels")

        # This just stores the name of the channel, currently pulling from only the first string after the original
        # command
        # I'd like to search for specific arguments like "-name" or similar - I'll need to use positional searches in
        # args to find the argument, then pull the item in the list directly following. Easy to do, my brain just
        # isn't ready right now
        c_name = str(args[0])

        # This creates the channel
        await guild.create_text_channel(c_name, category=cat)

        # This stores the new channel for the bot to message in later
        new_channel = discord.utils.get(guild.channels, name=c_name)

        # This sends a message in the new channel
        await new_channel.send("What are these... robuts?!")


client.run(os.getenv('DISCORD_TOKEN'))
