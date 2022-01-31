import functions.constants
import datetime
from classes.RaceRunner import RaceRunner
from classes.Race import Race

async def testcommand(message):
    """Do whatcha like"""
    if message.author.id not in functions.constants.ADMINS:
        return

    # Everything below here is up for grabs
    dmsg = "`\n"
    a = message.author
    ID = message.guild.id
    dmsg += f"Author:    {a} - Type: {type(a)}\n"
    dmsg += f"Author ID: {a.id} - Type: {type(a.id)}\n"
    dmsg += f"Guild:     {message.guild} - Type: {type(message.guild)}\n"
    dmsg += f"GuildID:   {message.guild.id} - Type: {type(message.guild.id)}\n"
    dmsg += f"Channel:   {message.channel} - Type: {type(message.channel)}\n"
    dmsg += f"Message Type: {type(message)}\n"

    dmsg += "\n"
    r = Race(message, message.channel)
    dmsg += str(r) + "\n"



    rr = RaceRunner()
    rr.member = a
    rr.guild = message.guild
    rr.channel = message.channel
    dmsg += str(rr)


    dmsg += "\n`"
    await message.channel.send(dmsg)
